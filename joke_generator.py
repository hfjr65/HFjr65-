"""
Random Joke Generator
=====================

A fun utility that fetches random jokes from external APIs.
Supports multiple joke sources and formats.

Author: HFjr65™ (Håkon Fløstad Jr.)
License: MIT
"""

import requests
import json
from typing import Dict, List, Optional
import time

class JokeGenerator:
    """Fetch and manage random jokes from various APIs."""
    
    # API endpoints
    APIS = {
        'official_joke_api': 'https://official-joke-api.appspot.com',
        'joke_ninjas': 'https://api.api-ninjas.com/v1/jokes',
        'dad_jokes': 'https://icanhazdadjoke.com',
        'jservice': 'https://jservice.io/api/random'
    }
    
    def __init__(self):
        """Initialize the joke generator."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HFjr65-JokeGenerator/1.0'
        })
        self.joke_cache = []
    
    def get_joke_from_official_api(self) -> Optional[Dict]:
        """Fetch a random joke from Official Joke API."""
        try:
            response = self.session.get(
                f"{self.APIS['official_joke_api']}/random_joke",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Official Joke API',
                'setup': data.get('setup', ''),
                'punchline': data.get('punchline', ''),
                'type': data.get('type', 'general'),
                'id': data.get('id', '')
            }
        except Exception as e:
            print(f"❌ Official Joke API Error: {e}")
            return None
    
    def get_joke_from_dad_jokes(self) -> Optional[Dict]:
        """Fetch a dad joke from icanhazdadjoke.com."""
        try:
            response = self.session.get(
                self.APIS['dad_jokes'],
                headers={'Accept': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Dad Jokes',
                'joke': data.get('joke', ''),
                'type': 'dad-joke',
                'id': data.get('joke', '').replace(' ', '_')[:20]
            }
        except Exception as e:
            print(f"❌ Dad Jokes API Error: {e}")
            return None
    
    def get_joke_from_jservice(self) -> Optional[Dict]:
        """Fetch a trivia question/answer from jService (Jeopardy)."""
        try:
            response = self.session.get(
                self.APIS['jservice'],
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if data:
                item = data[0]
                return {
                    'source': 'Jeopardy (jService)',
                    'category': item.get('category', {}).get('title', 'Unknown'),
                    'question': item.get('question', ''),
                    'answer': item.get('answer', ''),
                    'value': item.get('value', 0),
                    'type': 'trivia',
                    'id': item.get('id', '')
                }
        except Exception as e:
            print(f"❌ jService API Error: {e}")
            return None
    
    def get_random_joke(self, api_choice: Optional[str] = None) -> Optional[Dict]:
        """
        Fetch a random joke from a selected API.
        
        Parameters
        ----------
        api_choice : str, optional
            Choose specific API: 'official', 'dad_jokes', 'jservice'
            If None, randomly selects one.
        
        Returns
        -------
        Dict or None
            Joke data or None if API call fails
        """
        import random
        
        if api_choice is None:
            api_choice = random.choice(['official', 'dad_jokes', 'jservice'])
        
        print(f"🔄 Fetching joke from {api_choice}...")
        
        if api_choice == 'official':
            return self.get_joke_from_official_api()
        elif api_choice == 'dad_jokes':
            return self.get_joke_from_dad_jokes()
        elif api_choice == 'jservice':
            return self.get_joke_from_jservice()
        else:
            print(f"❌ Unknown API choice: {api_choice}")
            return None
    
    def format_joke_setup_punchline(self, joke: Dict) -> str:
        """Format setup/punchline style joke."""
        setup = joke.get('setup', '')
        punchline = joke.get('punchline', '')
        source = joke.get('source', 'Unknown')
        
        return f"""
╔══════════════════════════════════════╗
║ {source.center(36)} ║
╚══════════════════════════════════════╝

{setup}

... 🎭 ...

{punchline}

"""
    
    def format_joke_single_line(self, joke: Dict) -> str:
        """Format single-line joke."""
        joke_text = joke.get('joke', '')
        source = joke.get('source', 'Unknown')
        
        return f"""
╔══════════════════════════════════════╗
║ {source.center(36)} ║
╚══════════════════════════════════════╝

{joke_text}

"""
    
    def format_trivia(self, joke: Dict) -> str:
        """Format trivia/question style."""
        category = joke.get('category', 'Unknown')
        question = joke.get('question', '').replace('<i>', '').replace('</i>', '')
        answer = joke.get('answer', '').replace('<i>', '').replace('</i>', '')
        value = joke.get('value', 0)
        
        return f"""
╔══════════════════════════════════════╗
║ Jeopardy! - ${value} Question ║
║ Category: {category.center(26)} ║
╚══════════════════════════════════════╝

Q: {question}

... 🎯 ...

A: {answer}

"""
    
    def display_joke(self, joke: Dict) -> None:
        """Display a formatted joke."""
        if not joke:
            print("❌ No joke to display!")
            return
        
        joke_type = joke.get('type', 'unknown')
        
        if joke_type == 'dad-joke' or 'joke' in joke:
            print(self.format_joke_single_line(joke))
        elif joke_type == 'trivia':
            print(self.format_trivia(joke))
        elif 'setup' in joke and 'punchline' in joke:
            print(self.format_joke_setup_punchline(joke))
        else:
            print(f"Source: {joke.get('source', 'Unknown')}")
            print(json.dumps(joke, indent=2))
    
    def get_multiple_jokes(self, count: int = 5, api_choice: Optional[str] = None) -> List[Dict]:
        """
        Fetch multiple jokes.
        
        Parameters
        ----------
        count : int
            Number of jokes to fetch
        api_choice : str, optional
            Specific API to use
        
        Returns
        -------
        List[Dict]
            List of joke data
        """
        jokes = []
        for i in range(count):
            print(f"\n[Joke {i+1}/{count}]")
            joke = self.get_random_joke(api_choice)
            if joke:
                jokes.append(joke)
                self.display_joke(joke)
            time.sleep(0.5)  # Rate limiting
        
        return jokes
    
    def save_jokes_to_file(self, jokes: List[Dict], filename: str = 'jokes.json') -> None:
        """Save jokes to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jokes, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Jokes saved to '{filename}'")
        except Exception as e:
            print(f"❌ Error saving jokes: {e}")
    
    def stats(self) -> Dict:
        """Get statistics about cached jokes."""
        return {
            'cached_jokes': len(self.joke_cache),
            'available_apis': list(self.APIS.keys()),
            'total_requests': getattr(self, 'request_count', 0)
        }

def interactive_joke_menu():
    """Interactive menu for joke generator."""
    generator = JokeGenerator()
    
    print("\n" + "="*50)
    print("🎭 HFjr65™ RANDOM JOKE GENERATOR 🎭".center(50))
    print("="*50)
    print("\nAvailable APIs:")
    print("  1. Official Joke API (setup/punchline)")
    print("  2. Dad Jokes (icanhazdadjoke.com)")
    print("  3. Jeopardy Trivia (jService)")
    print("  4. Random mix (all APIs)")
    print("  5. Get 5 random jokes")
    print("  0. Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("\n👉 Choose option (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Thanks for laughing! Goodbye!")
                break
            
            elif choice == '1':
                joke = generator.get_random_joke('official')
                generator.display_joke(joke)
            
            elif choice == '2':
                joke = generator.get_random_joke('dad_jokes')
                generator.display_joke(joke)
            
            elif choice == '3':
                joke = generator.get_random_joke('jservice')
                generator.display_joke(joke)
            
            elif choice == '4':
                joke = generator.get_random_joke()  # Random API
                generator.display_joke(joke)
            
            elif choice == '5':
                jokes = generator.get_multiple_jokes(5)
                save = input("\n💾 Save jokes to file? (y/n): ").strip().lower()
                if save == 'y':
                    generator.save_jokes_to_file(jokes)
            
            else:
                print("❌ Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch':
            # Batch mode: get N jokes
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            api = sys.argv[3] if len(sys.argv) > 3 else None
            
            generator = JokeGenerator()
            jokes = generator.get_multiple_jokes(count, api)
            generator.save_jokes_to_file(jokes)
        
        elif sys.argv[1] == '--single':
            # Single joke mode
            api = sys.argv[2] if len(sys.argv) > 2 else None
            generator = JokeGenerator()
            joke = generator.get_random_joke(api)
            generator.display_joke(joke)
        
        elif sys.argv[1] == '--help':
            print("""
HFjr65™ Joke Generator
======================

Usage:
  python joke_generator.py              # Interactive mode
  python joke_generator.py --single [api]  # Single joke
  python joke_generator.py --batch [count] [api]  # Multiple jokes
  
APIs:
  - official (Official Joke API)
  - dad_jokes (Dad Jokes)
  - jservice (Jeopardy Trivia)
  
Examples:
  python joke_generator.py --single official
  python joke_generator.py --batch 10 dad_jokes
  python joke_generator.py --batch 5
            """)
        else:
            print("Unknown argument. Use --help for usage.")
    else:
        # Interactive mode
        interactive_joke_menu()

if __name__ == "__main__":
    main()
