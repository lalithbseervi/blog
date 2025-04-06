from django.http import HttpRequest
import random

def is_mobile_device(request: HttpRequest) -> bool:
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        mobile_keywords = ['iphone', 'android', 'windows phone', 'mobile', 'blackberry', 'ipad']
        return any(keyword in user_agent for keyword in mobile_keywords)

def is_ajax(request: HttpRequest) -> bool:
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def fetchQuote():
    quotes = [
        "If you prick us, do we not bleed? - Shakespeare",
        "When small men begin to cast big shadows, the sun is about to set. - Lin Yutang",
        "In the end I don't care if you love me or you hate me, just as long as I win. - House Of Cards",
        "Don't take the temperature for too long; you may forget to note down the values.",
        "You can beat 40 scholars with one fact, but you can't beat an idiot with 40 facts. - Mevlana",
        "A leader is best when people barely know he exists, when his work is done, his aim fulfilled, they will say: we did it ourselves. - Lao Tzu",
        "If the only tool you have is a hammer, everything looks like a nail.",
        "The man who asks a question is a fool for a minute, the man who does not ask is a fool for life. - Confucious",
        "Yesterday, I was clever, so I wanted to change the world. Today, I am cleverer, so I am changing myself.",
    ]

    quote = random.choice(quotes)

    return quote