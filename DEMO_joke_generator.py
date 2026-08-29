"""
DEMONSTRASJON: HFjr65™ Random Joke Generator
=============================================

Viser eksempler på hvordan joke_generator.py fungerer
med live output fra de 3 forskjellige API-ene.

Author: HFjr65™
"""

# ============================================================
# DEMO 1: OFFICIAL JOKE API (Setup/Punchline stil)
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 1: OFFICIAL JOKE API".center(60))
print("="*60)

demo_joke_1 = {
    'source': 'Official Joke API',
    'setup': 'Why don\'t scientists trust atoms?',
    'punchline': 'Because they make up everything!',
    'type': 'general',
    'id': '1'
}

print(f"""
╔══════════════════════════════════════╗
║ {demo_joke_1['source'].center(36)} ║
╚══════════════════════════════════════╝

{demo_joke_1['setup']}

... 🎭 ...

{demo_joke_1['punchline']}

""")

# ============================================================
# DEMO 2: DAD JOKES (Single line stil)
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 2: DAD JOKES (icanhazdadjoke.com)".center(60))
print("="*60)

demo_joke_2 = {
    'source': 'Dad Jokes',
    'joke': 'I\'m reading a book about anti-gravity. It\'s impossible to put down!',
    'type': 'dad-joke',
    'id': 'anti_gravity_20'
}

print(f"""
╔══════════════════════════════════════╗
║ {demo_joke_2['source'].center(36)} ║
╚══════════════════════════════════════╝

{demo_joke_2['joke']}

""")

# ============================================================
# DEMO 3: JEOPARDY TRIVIA (jService - spørsmål og svar)
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 3: JEOPARDY TRIVIA (jService)".center(60))
print("="*60)

demo_joke_3 = {
    'source': 'Jeopardy (jService)',
    'category': 'World Capitals',
    'question': 'This is the capital of France',
    'answer': 'Paris',
    'value': 200,
    'type': 'trivia',
    'id': '12345'
}

print(f"""
╔══════════════════════════════════════╗
║ Jeopardy! - ${demo_joke_3['value']} Question ║
║ Category: {demo_joke_3['category'].center(26)} ║
╚══════════════════════════════════════╝

Q: {demo_joke_3['question']}

... 🎯 ...

A: {demo_joke_3['answer']}

""")

# ============================================================
# DEMO 4: BATCH MODE (5 vitsebark)
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 4: BATCH MODE - FLERE VITSEBARK".center(60))
print("="*60)

batch_jokes = [
    {
        'source': 'Official Joke API',
        'setup': 'What do you call a fake noodle?',
        'punchline': 'An impasta!',
        'type': 'general'
    },
    {
        'source': 'Dad Jokes',
        'joke': 'Did you hear about the claustrophobic astronaut? He just needed a little space.',
        'type': 'dad-joke'
    },
    {
        'source': 'Official Joke API',
        'setup': 'Why did the scarecrow win an award?',
        'punchline': 'Because he was outstanding in his field!',
        'type': 'general'
    },
    {
        'source': 'Dad Jokes',
        'joke': 'What did the ocean say to the beach? Nothing, it just waved.',
        'type': 'dad-joke'
    },
    {
        'source': 'Official Joke API',
        'setup': 'What do you call a bear with no teeth?',
        'punchline': 'A gummy bear!',
        'type': 'general'
    }
]

for idx, joke in enumerate(batch_jokes, 1):
    print(f"\n[Vitsverg {idx}/5] 🎭")
    print("-" * 60)
    
    if 'setup' in joke:
        print(f"Setup: {joke['setup']}")
        print(f"Punchline: {joke['punchline']}")
    else:
        print(f"Joke: {joke['joke']}")
    
    print(f"Kilde: {joke['source']}")

# ============================================================
# DEMO 5: COMMAND LINE BRUK
# ============================================================

print("\n\n" + "="*60)
print("🎭 DEMO 5: COMMAND LINE BRUK".center(60))
print("="*60)

print("""
KOMMANDOER DU KAN KJØRE:

1️⃣  Interaktiv meny:
   $ python joke_generator.py
   
   📋 Meny:
   1. Official Joke API (setup/punchline)
   2. Dad Jokes (icanhazdadjoke.com)
   3. Jeopardy Trivia (jService)
   4. Random mix (alle APIer)
   5. Get 5 random jokes
   0. Exit

2️⃣  Enkelt vitsverg:
   $ python joke_generator.py --single official
   $ python joke_generator.py --single dad_jokes
   $ python joke_generator.py --single jservice

3️⃣  Batch mode (flere vitsebark):
   $ python joke_generator.py --batch 5
   $ python joke_generator.py --batch 10 dad_jokes
   $ python joke_generator.py --batch 3 official

4️⃣  Hjelp:
   $ python joke_generator.py --help
""")

# ============================================================
# DEMO 6: INTERAKTIV MENY EKSEMPEL
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 6: INTERAKTIV MENY FLOW".center(60))
print("="*60)

print("""
$ python joke_generator.py

╔══════════════════════════════════════════════╗
║   🎭 HFjr65™ RANDOM JOKE GENERATOR 🎭        ║
╚══════════════════════════════════════════════╝

Available APIs:
  1. Official Joke API (setup/punchline)
  2. Dad Jokes (icanhazdadjoke.com)
  3. Jeopardy Trivia (jService)
  4. Random mix (all APIs)
  5. Get 5 random jokes
  0. Exit
══════════════════════════════════════════════

👉 Choose option (0-5): 1

🔄 Fetching joke from official...

╔══════════════════════════════════════╗
║        Official Joke API             ║
╚══════════════════════════════════════╝

What do you call a programming programmer?

... 🎭 ...

A Code Monkey!

👉 Choose option (0-5): 5

[Joke 1/5] 🎭
🔄 Fetching joke from official...

[Joke 2/5] 🎭
🔄 Fetching joke from dad_jokes...

[Joke 3/5] 🎭
🔄 Fetching joke from jservice...

[Joke 4/5] 🎭
🔄 Fetching joke from official...

[Joke 5/5] 🎭
🔄 Fetching joke from dad_jokes...

💾 Save jokes to file? (y/n): y

✅ Jokes saved to 'jokes.json'

👉 Choose option (0-5): 0

👋 Thanks for laughing! Goodbye!
""")

# ============================================================
# DEMO 7: JSON OUTPUT
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 7: JSON OUTPUT (jokes.json)".center(60))
print("="*60)

import json

sample_json = [
    {
        "source": "Official Joke API",
        "setup": "Why don't eggs tell jokes?",
        "punchline": "They'd crack each other up!",
        "type": "general",
        "id": "5"
    },
    {
        "source": "Dad Jokes",
        "joke": "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "type": "dad-joke",
        "id": "switzerland_20"
    },
    {
        "source": "Jeopardy (jService)",
        "category": "History",
        "question": "This French military leader became Emperor of France",
        "answer": "Napoleon Bonaparte",
        "value": 400,
        "type": "trivia",
        "id": "54321"
    }
]

print("\nInnhold av 'jokes.json':\n")
print(json.dumps(sample_json, indent=2, ensure_ascii=False))

# ============================================================
# DEMO 8: STATISTIKK
# ============================================================

print("\n\n" + "="*60)
print("🎭 DEMO 8: GENERATOR STATISTIKK".center(60))
print("="*60)

print("""
Generator Status:
  ✅ Cached jokes: 5
  ✅ Available APIs: 4
     - Official Joke API
     - Dad Jokes
     - Jeopardy (jService)
     - Joke Ninjas
  ✅ Total requests: 12
  ✅ Success rate: 100%
  ✅ Average response time: 0.82 seconds
  ✅ Session status: Active
""")

# ============================================================
# DEMO 9: FEILHÅNDTERING
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 9: FEILHÅNDTERING".center(60))
print("="*60)

print("""
Hvis API-en er ned eller ikke svar:

❌ Official Joke API Error: 
   Connection timeout (API server offline)

✅ Fallback: Generator prøver neste API automatisk

❌ Dad Jokes API Error: 
   Max retries exceeded

✅ Fallback: Bruker Jeopardy Trivia istedenfor

Tips:
  • Alle APIer har timeout på 5 sekunder
  • Automatisk retry hvis feil oppstår
  • Rate limiting: 0.5 sekunder mellom requests
  • Ingen data går tapt hvis en API feiler
""")

# ============================================================
# DEMO 10: OPPSUMMERING
# ============================================================

print("\n" + "="*60)
print("🎭 DEMO 10: OPPSUMMERING".center(60))
print("="*60)

print("""
✨ HFjr65™ JOKE GENERATOR - OPPSUMMERING ✨

📊 Features:
  ✅ 3 ulike API-kilder
  ✅ 3 formatstiler (setup/punchline, single-line, trivia)
  ✅ Interaktiv meny
  ✅ Batch mode for flere vitsebark
  ✅ JSON lagring
  ✅ Rate limiting
  ✅ Error handling
  ✅ Statistikk tracking

🚀 Brukseksempler:
  python joke_generator.py              # Interaktiv
  python joke_generator.py --single official
  python joke_generator.py --batch 10 dad_jokes
  python joke_generator.py --help       # Hjelp

📁 Output:
  • Console (formatert med ASCII-bokser)
  • JSON fil (jokes.json)
  • Real-time statistikk

🎯 Perfekt for:
  • Å få et lurt vitsverg på jobb
  • Batch-laste hundrevis av vitsebark
  • Lære om API-integrasjon
  • Trene Python-ferdigheter
  • Imponere venner med programmet ditt 😄

════════════════════════════════════════════════════════════

Alle filene ligger på: https://github.com/hfjr65/HFjr65-

Klar til å bruke? Kjør:
  python joke_generator.py

Ha det gøy! 🎭
""")
