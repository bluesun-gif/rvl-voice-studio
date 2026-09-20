"""
Relief Validation Limited (RVL) Master Corporate Knowledge Base
Authoritative, verified data for bilingual AI Voice Agents & RAG systems.
Part of Deepon Group ecosystem: RVL, DGePay Services Limited, DigiInfotech Limited.
"""

RVL_MASTER_KNOWLEDGE = {
    "company": {
        "legal_name": "Relief Validation Limited",
        "short_name": "RVL",
        "parent_group": "Deepon Group",
        "affiliates": ["DGePay Services Limited", "DigiInfotech Limited"],
        "license_status": "Licensed Certifying Authority (CA) of the Government of Bangladesh",
        "governing_law": "Information and Communication Technology (ICT) Act 2006 (Amended 2013)",
        "regulatory_body": "Office of the Controller of Certifying Authorities (CCA), Ministry of Posts, Telecommunications and Information Technology, Government of the People's Republic of Bangladesh",
        "headquarters": {
            "building": "Rangs FC Square, Level-5",
            "address": "Plot-6/A, Road-32, Gulshan Avenue, Gulshan-1",
            "city": "Dhaka-1212",
            "country": "Bangladesh"
        },
        "contact": {
            "hotline": "+8809606501231",
            "email": "info@reliefvalidation.com.bd",
            "website": "https://www.reliefvalidation.com.bd",
            "oneid_portal": "https://oneid.com.bd"
        },
        "leadership": "Managing Director / CEO (Rashed sir)"
    },

    "products": {
        "vds": {
            "name": "VDS (Visible Digital Seal)",
            "branding_rule": "CRITICAL: ALWAYS refer to it as 'VDS' or 'VDS QR' - Powered by Relief Validation Ltd. NEVER say 'DGePay VDS'.",
            "what_it_is": "A high-density 2D cryptographic barcode (seal) printed or embedded on official documents such as bank statements, solvency certificates, loan sanction letters, trade finance documents, and educational certificates.",
            "problem_solved": "Eliminates forged paper bank statements and fake solvency certificates commonly presented for student visas, embassies, and bank loan approvals.",
            "technology": "Uses asymmetric public-key cryptography (PKI) and X.509 digital signatures under Bangladesh ICT Act 2006 legal compliance.",
            "verification_speed": "Verifiable in under 5 seconds.",
            "offline_capability": "100% verifiable offline via VeriQR app without pinging central databases, protecting banking client data secrecy."
        },
        "veriqr": {
            "name": "VeriQR™",
            "type": "Mobile Verifier Application (iOS & Android)",
            "function": "Scans and cryptographically decodes VDS digital seals on bank statements and official certificates.",
            "key_benefits": [
                "Instant verification in under 5 seconds",
                "Operates completely offline without sending customer data to any server",
                "Detects any tampering, alteration of balance, date, or account holder name",
                "Used by embassies, visa officers, commercial banks, and verification officers"
            ]
        },
        "oneid": {
            "name": "OneID Wallet",
            "domain": "oneid.com.bd",
            "tagline": "Bangladesh's National Digital Credential Vault (similar to India's DigiLocker)",
            "function": "Enables citizens and students to store, verify, and share educational certificates (SSC, HSC, Board/University transcripts) and personal credentials attestation-free.",
            "user_benefit": "Zero physical paperwork, instant paperless verification for job applications and higher study."
        },
        "verifyid": {
            "name": "VerifyID eKYC",
            "function": "AI-powered optical character recognition (OCR), facial matching, liveness detection, and National ID (NID) biometric verification for instant customer onboarding in commercial banks and MFS."
        },
        "dgepay": {
            "name": "DGePay Services Limited",
            "function": "Fintech payment processing, merchant POS services, digital transactions, and Tally Khata bookkeeping automation for retailers and SMEs across Bangladesh."
        },
        "digiinfotech": {
            "name": "DigiInfotech & Deepon Group",
            "function": "Enterprise software engineering, systems integration, energy, infrastructure, and nationwide digital transformation."
        }
    }
}

# Formatted Knowledge Prompt for LLM Context
RVL_PROMPT_KNOWLEDGE_TEXT = """
OFFICIAL CORPORATE PROFILE & KNOWLEDGE BASE:
- Company: Relief Validation Limited (RVL)
- Parent Group: Deepon Group | Allied Fintech: DGePay Services Limited | Allied Tech: DigiInfotech Limited
- Legal Authority: Licensed Certifying Authority (CA) of Bangladesh under ICT Act 2006, regulated by CCA Bangladesh (Ministry of Posts & Telecom).
- Corporate HQ: Rangs FC Square, Level-5, Plot-6/A, Road-32, Gulshan Avenue, Gulshan-1, Dhaka-1212.
- Helpline / Contact: +8809606501231 (09606501231) | info@reliefvalidation.com.bd | www.reliefvalidation.com.bd
- Leadership: Managing Director / CEO (Rashed sir).

PRODUCTS & STRICT BRANDING RULES:
1. VDS (Visible Digital Seal):
   - In Bengali: "ভিজিবল ডিজিটাল সিল" (Visible Digital Seal - বাংলায় 'ভিজিবল ডিজিটাল সিল' বলবেন).
   - Cryptographic 2D digital seal for bank statements, solvency certificates, loan sanction letters, trade finance, and embassy submissions.
   - Completely prevents document forgery and fake bank statement fraud in Bangladesh.
   - Verifiable in under 5 seconds.
   - 100% offline verification via VeriQR app without central database connection, ensuring complete banking secrecy.
   - STRICT BRAND RULE: NEVER say "DGePay VDS". The product is simply "VDS" or "VDS QR" (Powered by Relief Validation Ltd).

2. VeriQR™ App:
   - Mobile verification app (iOS and Android).
   - Scans and decrypts VDS cryptographic seals in less than 5 seconds without internet connection.
   - Ideal for foreign embassies, visa processing centers, and loan verification officers.

3. OneID Wallet (oneid.com.bd):
   - Bangladesh's digital credential vault (equivalent to DigiLocker).
   - Stores and verifies SSC, HSC, and university transcripts attestation-free.

4. VerifyID eKYC:
   - AI biometric face match, liveness detection, and NID extraction for banking customer onboarding.

5. DGePay Services Limited:
   - Digital payments platform and merchant Tally Khata ledger integration for retail stores and SMEs.

6. DigiInfotech & Deepon Group:
   - Enterprise IT solutions, digital transformation, and telecom/energy engineering.
"""

SYSTEM_VOICE_INSTRUCTIONS = """
YOU ARE: The bilingual Voice AI representative for 'Relief Validation Limited' (RVL) on a live phone call.
YOUR GOAL: Provide helpful, confident, clear corporate answers about RVL, VDS, VeriQR, and OneID.

CRITICAL VOICE CONVERSATION RULES:
1. DUAL LANGUAGE HANDLING:
   - If caller speaks Bengali: Respond in natural, polite Dhaka Bengali (মার্জিত ও আন্তরিক বাংলা).
   - If caller speaks English: Respond in crisp, articulate corporate English.
2. BREVITY (CALLER PACING):
   - Speak only 1 or 2 concise sentences per turn (maximum 35-40 words).
   - Do not overwhelm the caller. Deliver the answer, then pause naturally for their reply.
3. PRONUNCIATION PHONETICS:
   - For English acronyms when speaking Bengali, use natural phonetics:
     VDS -> ভি ডি এস
     VeriQR -> ভেরি কিউআর
     OneID -> ওয়ানআইডি
     ICT Act -> আইসিটি অ্যাক্ট
4. FORMAT RESTRICTIONS:
   - NEVER use markdown, asterisk (*), hashes (#), dashes (-), or bullet points.
   - Output plain spoken prose ONLY.
"""

FALLBACK_KNOWLEDGE_QA = [
    {
        "keywords": ["অনলাইন", "অফলাইন", "ইন্টারনেট", "online", "offline", "internet", "সার্ভার ছাড়া"],
        "bn": "আমাদের ভেরিফিকেশন সিস্টেমটি সম্পূর্ণ অফলাইনে কাজ করে। ইন্টারনেট সংযোগ ছাড়াই ভেরি কিউআর মোবাইল অ্যাপ দিয়ে যেকোনো ব্যাংক স্টেটমেন্ট বা ডকুমেন্টের ভি ডি এস সিল মাত্র ৫ সেকেন্ডে শতভাগ নির্ভুলভাবে যাচাই করা যায়।",
        "en": "Our verification system operates completely offline. Using the VeriQR app, VDS seals on bank statements and documents can be verified in under 5 seconds without requiring any internet connection."
    },
    {
        "keywords": ["ভিডিএস", "ভি ডি এস", "vds", "visible digital seal", "ডিজিটাল সিল", "ভেজিটেবিল"],
        "bn": "ভিজিবল ডিজিটাল সিল বা ভি ডি এস হলো ব্যাংক স্টেটমেন্ট ও আর্থিক সনদের জন্য একটি ক্রিপ্টোগ্রাফিক ডিজিটাল সিল, যা ডকুমেন্ট জালিয়াতি সম্পূর্ণ বন্ধ করে এবং ৫ সেকেন্ডে যাচাই করা যায়।",
        "en": "Visible Digital Seal (VDS) is a high-security cryptographic 2D digital seal that completely eliminates document tampering on bank statements and solvency certificates."
    },
    {
        "keywords": ["ভেরি কিউআর", "ভেরিকিউআর", "veriqr", "স্ক্যান", "মোবাইল অ্যাপ"],
        "bn": "ভেরি কিউআর হলো আমাদের মোবাইল অ্যাপ, যার মাধ্যমে ইন্টারনেট ছাড়াই যেকোনো ব্যাংক স্টেটমেন্ট বা সার্টিফিকেটের ভি ডি এস ডিজিটাল সিল স্ক্যান করে তাৎক্ষণিক সত্যতা যাচাই করা যায়।",
        "en": "VeriQR is our mobile verification app for iOS and Android that validates VDS seals offline in under 5 seconds without accessing a central server."
    },
    {
        "keywords": ["ওয়ানআইডি", "ওয়ান আইডি", "oneid", "সার্টিফিকেট", "বোর্ড", "vault", "ডিজিলকার", "ডিজিটাল ভল্ট"],
        "bn": "ওয়ানআইডি ওয়ালেট হলো বাংলাদেশের জাতীয় ডিজিটাল ভল্ট, যেখানে নাগরিক এবং শিক্ষার্থীরা কোনোপ্রকার সত্যায়ন ছাড়াই তাদের এসএসসি, এইচএসসি ও ডিগ্রির সার্টিফিকেট নিরাপদে সংরক্ষণ ও শেয়ার করতে পারেন।",
        "en": "OneID Wallet is Bangladesh's national digital credential vault, allowing citizens and students to store and share verified educational certificates attestation-free."
    },
    {
        "keywords": ["ঠিকানা", "অফিস", "কোথায়", "যোগাযোগ", "address", "location", "office", "contact", "ফোন", "নাম্বার"],
        "bn": "রিলিফ ভ্যালিডেশন লিমিটেডের প্রধান কার্যালয় গুলশান-১, ঢাকার রংস এফসি স্কয়ারের লেভেল-৫ এ অবস্থিত। আমাদের সাথে যোগাযোগের হটলাইন নম্বর ০৯৬০৬৫০১২৩১।",
        "en": "Relief Validation Limited headquarters is located at Rangs FC Square, Level-5, Gulshan-1, Dhaka-1212. You can contact us at +8809606501231."
    },
    {
        "keywords": ["লাইসেন্স", "আইন", "আইসিটি", "ict", "cca", "কর্তৃপক্ষ", "অনুমোদন"],
        "bn": "রিলিফ ভ্যালিডেশন লিমিটেড বাংলাদেশ সরকারের তথ্যপ্রযুক্তি আইন ২০০৬-এর অধীনে নিয়ন্ত্রক সংস্থা সিসিএ কর্তৃক লাইসেন্সপ্রাপ্ত একটি অনুমোদিত সার্টিফাইং অথরিটি।",
        "en": "Relief Validation Limited is an authorized Certifying Authority (CA) licensed by the Government of Bangladesh under the ICT Act 2006, regulated by the CCA."
    },
    {
        "keywords": ["ডিজিপে", "dgepay", "টালি", "খাতা", "পেমেন্ট", "মার্চেন্ট"],
        "bn": "ডিজিপে সার্ভিসেস লিমিটেড হলো আমাদের সহযোগী ফিনটেক প্ল্যাটফর্ম, যা খুচরা ব্যবসায়ী ও মার্চেন্টদের জন্য ডিজিটাল লেনদেন এবং টালিখাতা স্বয়ংক্রিয় করার সুবিধা প্রদান করে।",
        "en": "DGePay Services Limited is our allied fintech platform offering merchant digital payments and Tally Khata bookkeeping automation."
    }
]

def get_smart_fallback(query: str, lang: str = "bn") -> str:
    if not query:
        return "রিলিফ ভ্যালিডেশন লিমিটেডে আপনাকে স্বাগতম। আমি কীভাবে আপনাকে সহায়তা করতে পারি?" if lang == "bn" else "Welcome to Relief Validation Limited. How may I assist you today?"
    
    q_lower = query.lower()
    for item in FALLBACK_KNOWLEDGE_QA:
        for kw in item["keywords"]:
            if kw.lower() in q_lower:
                return item["bn"] if lang == "bn" else item["en"]
                
    if lang == "bn":
        return "রিলিফ ভ্যালিডেশন লিমিটেড তথ্যপ্রযুক্তি আইন ২০০৬-এর অধীনে লাইসেন্সপ্রাপ্ত সিএ। আমরা ভি ডি এস ও ভেরি কিউআর দিয়ে ডকুমেন্টের শতভাগ নিরাপত্তা নিশ্চিত করি।"
    return "Relief Validation Limited is a Licensed Certifying Authority under the ICT Act 2006, providing VDS and VeriQR solutions for document fraud prevention."
