from django.contrib import admin
from .models import Conversation, Member, Message, Receiver

class MemberInline(admin.TabularInline):
    model = Member

class ReceiverInline(admin.TabularInline):
    model = Receiver

class MessageAdmin(admin.ModelAdmin):
    inlines = [ReceiverInline]
    list_display = ('conversation', 'sender', 'text', 'created_at', 'updated_at')

class ConversationAdmin(admin.ModelAdmin):
    inlines = [MemberInline]
    list_display = ('name', 'type', 'created_by', 'created_at', 'updated_at')
    list_filter = ('type',)
    search_fields = ('name', 'description', 'created_by')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'user')

class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'read', 'received_at')

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Receiver, ReceiverAdmin)
