from rest_framework import serializers
from umoney.models import UmoneyReq


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     card_number = serializers.CharField(required=True, allow_blank=False, max_length=16)
#     card_algorithm_id = serializers.CharField(required=True, allow_blank=False, max_length=2)
#     card_keyset_v = serializers.CharField(required=True, allow_blank=False, max_length=2)
#     card_transaction_seq_number = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     card_random_number = serializers.CharField(required=True, allow_blank=False, max_length=16)
#     card_balance = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     topup_amount = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     sign1 = serializers.CharField(required=True, allow_blank=False, max_length=8)
#     comment = serializers.CharField(required=False, allow_blank=True, max_length=100)

#     def create(self, validated_data):
#         """
#         Create and return a new `UmoneyReq` instance, given the validated data.
#         """
#         return UmoneyReq.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance

class UmoneyReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmoneyReq
        fields = [
            'id', 
            'card_number', 
            'card_algorithm_id', 
            'card_keyset_v', 
            'card_transaction_seq_number', 
            'card_random_number', 
            'card_balance',
            'topup_amount',
            'sign1',
            'comment',
            'created'
            ]