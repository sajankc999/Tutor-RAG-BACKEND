from content.models import Content
from rest_framework import serializers

class ContentSerializer(serializers.ModelSerializer):
    page_content= serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    class Meta:
        model=Content
        fields=(
            "id",
            "page_content",
            "metadata"
        )

    def get_metadata(self,obj):
        return {
            "topic":obj.topic,
            "title":obj.title,
            "grade":obj.grade
        }
    
    def get_page_content(self,obj):
        if obj.file:
            obj.file.open(mode='r')
            try:
                return obj.file.read()
            except:
                return None
            finally:
                obj.file.close()
        return None