from rest_framework import serializers
from chatshell.models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ChatHistory
        fields=(
            "id",
            "user_prompt",
            "generated_response",
            "generated_time",        
        )

class AskQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    metadata_filter = serializers.DictField(required=False)
