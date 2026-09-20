# -*- coding: utf-8 -*-
"""
Bangla Phonetic Normalizer for Edge-TTS
Converts English loan words, technical terms, acronyms, and digits into 
phonetically accurate Bengali so bn-BD-NabanitaNeural speaks with 100% natural Dhaka pronunciation.
"""
import re

# Acronyms & technical terms mapped to Bengali phonetic script
REPLACEMENTS = [
    (r'\bRelief Validation Limited\b', 'রিলিফ ভ্যালিডেশন লিমিটেড'),
    (r'\bRelief Validation\b', 'রিলিফ ভ্যালিডেশন'),
    (r'\bRVL\b', 'আর ভি এল'),
    (r'\bVisible Digital Seal\b', 'ভিজিবল ডিজিটাল সিল'),
    (r'\bVisible\b', 'ভিজিবল'),
    (r'ভেজিটেবিল', 'ভিজিবল'),
    (r'\bVDS\b', 'ভি ডি এস'),
    (r'\bVeriDoc\b', 'ভেরি ডক'),
    (r'\bVeriQR\b', 'ভেরি কিউআর'),
    (r'\bVeri-QR\b', 'ভেরি কিউআর'),
    (r'\bVeri QR\b', 'ভেরি কিউআর'),
    (r'\bVeri\b', 'ভেরি'),
    (r'\bVER\b', 'ভেরি'),
    (r'\bOneID Wallet\b', 'ওয়ান আইডি ওয়ালেট'),
    (r'\bOneID\b', 'ওয়ান আইডি'),
    (r'\bOne ID\b', 'ওয়ান আইডি'),
    (r'\bWallet\b', 'ওয়ালেট'),
    (r'\bDGePay Services Limited\b', 'ডিজিপে সার্ভিসেস লিমিটেড'),
    (r'\bDGePay\b', 'ডিজিপে'),
    (r'\bDGPay\b', 'ডিজিপে'),
    (r'\bDigiInfotech Limited\b', 'ডিজি ইনফোটেক লিমিটেড'),
    (r'\bDigiInfotech\b', 'ডিজি ইনফোটেক'),
    (r'\bDeepon Group\b', 'দিপন গ্রুপ'),
    (r'\bDeepon\b', 'দিপন'),
    (r'\bDipon\b', 'দিপন'),
    (r'\bICT Act 2006\b', 'আইসিটি অ্যাক্ট ২০০৬'),
    (r'\bICT Act\b', 'আইসিটি অ্যাক্ট'),
    (r'\bCCA\b', 'সি সি এ'),
    (r'\bQR Code\b', 'কিউ আর কোড'),
    (r'\bQR\b', 'কিউ আর'),
    (r'\beKYC\b', 'ই কে ওয়াই সি'),
    (r'\bKYC\b', 'কে ওয়াই সি'),
    (r'\bNID\b', 'এন আই ডি'),
    (r'\bAI\b', 'এ আই'),
    (r'\bAPI\b', 'এ পি আই'),
    (r'\bAPIs\b', 'এ পি আই'),
    (r'\bPKI\b', 'পি কে আই'),
    (r'\bSSC\b', 'এস এস সি'),
    (r'\bHSC\b', 'এইচ এস সি'),
    (r'\bBank Solvency Certificate\b', 'ব্যাংক সলভেন্সি সার্টিফিকেট'),
    (r'\bBank Solvency\b', 'ব্যাংক সলভেন্সি'),
    (r'\bSolvency Certificate\b', 'সলভেন্সি সার্টিফিকেট'),
    (r'\bBank Statement\b', 'ব্যাংক স্টেটমেন্ট'),
    (r'\bBank Statements\b', 'ব্যাংক স্টেটমেন্ট'),
    (r'\bBank\b', 'ব্যাংক'),
    (r'\bBanks\b', 'ব্যাংকগুলো'),
    (r'\bDigital Seal\b', 'ডিজিটাল সিল'),
    (r'\bDigital\b', 'ডিজিটাল'),
    (r'\bSeal\b', 'সিল'),
    (r'\bOnline\b', 'অনলাইন'),
    (r'\bOffline\b', 'অফলাইন'),
    (r'\bWebsite\b', 'ওয়েবসাইট'),
    (r'\bPortal\b', 'পোর্টাল'),
    (r'\bApp\b', 'অ্যাপ'),
    (r'\bApps\b', 'অ্যাপস'),
    (r'\bApp Store\b', 'অ্যাপ স্টোর'),
    (r'\bPlay Store\b', 'প্লে স্টোর'),
    (r'\bTally Khata\b', 'টালি খাতা'),
    (r'\bTally\b', 'টালি'),
    (r'\bSME\b', 'এস এম ই'),
    (r'\bSMEs\b', 'এস এম ই'),
    (r'\bLoan Sanction Letter\b', 'লোন স্যাংশন লেটার'),
    (r'\bLoan\b', 'লোন'),
    (r'\bVerification\b', 'ভেরিফিকেশন'),
    (r'\bVerify\b', 'ভেরিফাই'),
    (r'\bVerified\b', 'ভেরিফাইড'),
    (r'\bAuthentic\b', 'অথেন্টিক'),
    (r'\bFraud\b', 'জালিয়াতি'),
    (r'\bTamper-proof\b', 'জালিয়াতি মুক্ত'),
    (r'\bSecurity\b', 'সিকিউরিটি'),
    (r'\bSystem\b', 'সিস্টেম'),
    (r'\bDemo\b', 'ডেমো'),
    (r'\bHotline\b', 'হটলাইন'),
    (r'\bCall\b', 'কল'),
    (r'\b5 seconds\b', 'পাঁচ সেকেন্ড'),
    (r'\b5 second\b', 'পাঁচ সেকেন্ড'),
    (r'\b5s\b', 'পাঁচ সেকেন্ড'),
    (r'\b24/7\b', 'সার্বক্ষণিক'),
    (r'\b24 hours\b', 'চব্বিশ ঘণ্টা'),
    (r'\bSMS\b', 'এস এম এস'),
    (r'\bEmail\b', 'ইমেইল'),
]

# Bengali digits mapping
BN_DIGITS = {
    '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
    '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
}

def normalize_bangla_for_tts(text: str) -> str:
    """
    Cleans up text before feeding into Edge-TTS Bangla voice.
    Replaces English technical terms with Bangla phonetic equivalents.
    """
    if not text:
        return ""

    # Check if text contains any Bangla characters
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', text))
    if not has_bangla:
        return text

    result = text
    for pattern, repl in REPLACEMENTS:
        result = re.sub(pattern, repl, result, flags=re.IGNORECASE)

    # Convert standalone ASCII digits into Bengali digits for smoother reading
    def replace_num(match):
        digits = match.group(0)
        return "".join(BN_DIGITS.get(d, d) for d in digits)

    result = re.sub(r'\d+', replace_num, result)

    # Clean double spaces
    result = re.sub(r'\s+', ' ', result).strip()
    return result
