from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, FlexSendMessage, FollowEvent, UnfollowEvent

from line_bot.flex_message_json import shop_information_json, attractions_information_json, bill_information_json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
line_bot_api2 = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN2)
parser2 = WebhookParser(settings.LINE_CHANNEL_SECRET2)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # 呼叫函式回傳資訊
        for event in events:
            # print('BotTest_group_id:', event.source.group_id)
            # print('BotTest_user_id:', event.source.user_id)
            if isinstance(event, MessageEvent) and event.message.text == '店家資訊':
                flex_message = create_shop_information()
                line_bot_api.reply_message(event.reply_token, flex_message)
            elif isinstance(event, MessageEvent) and event.message.text == '景點資訊':
                flex_message = create_attractions_information()
                line_bot_api.reply_message(event.reply_token, flex_message)
            # elif isinstance(event, MessageEvent) and event.message.text == '帳單資訊':
            #     flex_message = create_bill_information()
            #     line_bot_api.reply_message(event.reply_token, flex_message)
            elif isinstance(event, MessageEvent) and event.message.text == '帳單資訊':
                user_id = event.source.user_id
                group_user(user_id)
            elif isinstance(event, FollowEvent):
                followUserId = event.source.user_id
                print('followUserId : ', followUserId)
            elif isinstance(event, UnfollowEvent):
                unfollowUserId = event.source.user_id
                print('unfollowUserId : ', unfollowUserId)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
@csrf_exempt
def callback2(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser2.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # 呼叫函式回傳資訊
        for event in events:
            print('BotTest2_user_id:', event.source.user_id)
            if isinstance(event, MessageEvent) and event.message.text == '店家資訊':
                flex_message = create_shop_information()
                line_bot_api2.reply_message(event.reply_token, flex_message)
            elif isinstance(event, MessageEvent) and event.message.text == '景點資訊':
                flex_message = create_attractions_information()
                line_bot_api2.reply_message(event.reply_token, flex_message)
            # elif isinstance(event, MessageEvent) and event.message.text == '帳單資訊':
            #     flex_message = create_bill_information()
            #     line_bot_api.reply_message(event.reply_token, flex_message)
            elif isinstance(event, MessageEvent) and event.message.text == '帳單資訊':
                user_id = event.source.user_id
                group_user2(user_id)
            elif isinstance(event, FollowEvent):
                followUserId = event.source.user_id
                print('followUserId : ', followUserId)
            elif isinstance(event, UnfollowEvent):
                unfollowUserId = event.source.user_id
                print('unfollowUserId : ', unfollowUserId)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# 回傳文字
def handle_text_message(event):
    message = TextSendMessage(text='您發送了訊息：' + event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

# 回傳個人資訊
def group_user(user_id):
    user_profile = line_bot_api.get_profile(user_id)
    user_name = user_profile.display_name
    user_image = user_profile.picture_url
    user_status_message = user_profile.status_message
    message = f'Hello, {user_name}!\nThis is your image:\n{user_image}\nThis is your status_massage:\n{user_status_message}'
    line_bot_api.push_message(user_id, TextSendMessage(text=message))

def group_user2(user_id):
    user_profile = line_bot_api.get_profile(user_id)
    user_name = user_profile.display_name
    user_image = user_profile.picture_url
    user_status_message = user_profile.status_message
    message = f'Hello, {user_name}!\nThis is your image:\n{user_image}\nThis is your status_massage:\n{user_status_message}'
    line_bot_api2.push_message(user_id, TextSendMessage(text=message))

# 回傳利用flex message創建的店家資訊
def create_shop_information():
# 使用 flex_message_json 創建 Flex Message
    flex_message = FlexSendMessage(
        alt_text="Flex Message Example",
        contents=shop_information_json
    )
    return flex_message

# 回傳利用flex message創建的景點資訊
def create_attractions_information():
# 使用 flex_message_json 創建 Flex Message
    flex_message = FlexSendMessage(
        alt_text="Flex Message Example",
        contents=attractions_information_json
    )
    return flex_message

# 回傳利用flex message創建的帳單資訊
def create_bill_information():
# 使用 flex_message_json 創建 Flex Message
    flex_message = FlexSendMessage(
        alt_text="Flex Message Example",
        contents=bill_information_json
    )
    return flex_message

# 測試在同一個provider底下的不同channel內同一個使用者的user_id會是相同的
# user_id = 'Ue4f9cc74a78774e316dee28372f2b820'
# group_id = 'Cf2ba19b5724a62b35511b08cb5bd890e'
# message = TextSendMessage(text='Hello, this is a test message.')
# line_bot_api.push_message(user_id, message)
# line_bot_api2.push_message(user_id, message)

# 抓取群組所有成員user_id(權限不足)
# group_id = 'Cf2ba19b5724a62b35511b08cb5bd890e'
# try:
#     member_ids = line_bot_api.get_group_member_ids(group_id)
#     # member_ids 是包含群组成员user_id的列表
#     for user_id in member_ids:
#         print(f'User ID: {user_id}')
# except Exception as e:
#     print(f'Error: {e}')

def indexRouter(request):
    return render(request, 'index.html')