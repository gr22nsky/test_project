from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.settings import OPENAI_API_KEY
from .models import Conversation, AI_Friend
import openai

openai.api_key = OPENAI_API_KEY

class ChatbotResponseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        ai_friend_id = request.data.get("ai_friend_id")
        
        if not user_message or not ai_friend_id:
            return Response({"error": "Message and AI friend ID are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            ai_friend = AI_Friend.objects.get(id=ai_friend_id)

            ai_friend_description = ai_friend.description

            previous_conversations = Conversation.objects.filter(
                user_id=request.data['user_id'], ai_friend=ai_friend
            ).values_list('message', flat=True)

            if not previous_conversations:
                previous_conversations = ["This is the first conversation."]

            conversation_history = "\n".join(previous_conversations)
            template = """system: Answer the User's new message based on the following Description and Previous Conversations.
                        Description: {ai_friend_description}
                        Previous Conversations: {conversation_history}
                        User's new message: {user_message}"""
            prompt = ChatPromptTemplate.from_template(template)

            # filled_prompt = template.format(
            #     ai_friend_description=ai_friend_description,
            #     conversation_history=conversation_history,
            #     user_message=user_message
            # )
            # print(filled_prompt)

            llm = ChatOpenAI(model='gpt-4o-mini', temperature=1)
            conversation_chain = prompt | llm
            ai_response = conversation_chain.invoke({
                'user_message': user_message,
                'ai_friend_description': ai_friend_description,
                'conversation_history': conversation_history
            }).content

            Conversation.objects.create(
                user_id=request.data['user_id'],
                ai_friend=ai_friend,
                message={'user_message' : user_message, 'ai_response' : ai_response}
            )

            return Response(ai_response, status=status.HTTP_200_OK)

        except AI_Friend.DoesNotExist:
            return Response({"error": "AI friend not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
