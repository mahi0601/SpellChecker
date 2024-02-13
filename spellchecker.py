import tkinter as tk
from tkinter import messagebox
import concurrent.futures
import asyncio
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_within_distance(self, word, max_distance):
        suggestions = []
        stack = [(self.root, '', 0)]

        while stack:
            node, current_prefix, distance = stack.pop()

            if distance > max_distance:
                continue

            if node.is_end_of_word:
                suggestions.append(current_prefix)

            for char, child_node in node.children.items():
                stack.append((child_node, current_prefix + char, distance + 1))

        return suggestions

class SpellChecker:
    def __init__(self, dictionary):
        self.trie = Trie()
        self.build_trie(dictionary)

    def build_trie(self, dictionary):
        for word in dictionary:
            self.trie.insert(word)

    def symmetric_delete_distance(self, word1, word2, max_distance):
        if len(word1) < len(word2):
            word1, word2 = word2, word1

        previous_row = range(len(word2) + 1)

        for i, char1 in enumerate(word1):
            current_row = [i + 1]
            for j, char2 in enumerate(word2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (char1 != char2)

                current_row.append(min(insertions, deletions, substitutions))

            if min(current_row) > max_distance:
                return float('inf')

            previous_row = current_row

        return previous_row[-1]

    def suggest_correction(self, word, max_distance=3):
        suggestions = self.trie.search_within_distance(word, max_distance)

        min_distance = float('inf')
        best_match = None

        for candidate in suggestions:
            distance = self.symmetric_delete_distance(word, candidate, max_distance)
            if distance < min_distance:
                min_distance = distance
                best_match = candidate

        return best_match

def measure_response_time(spell_checker, words):
    start_time = time.time()

    for word in words:
        _ = spell_checker.suggest_correction(word)

    end_time = time.time()
    elapsed_time = end_time - start_time

    words_processed = len(words)
    response_time_per_1000_words = (elapsed_time / words_processed) * 1000

    return response_time_per_1000_words

async def async_spell_check(spell_checker, words, result_queue):
    for word in words:
        correction = spell_checker.suggest_correction(word)
        result_queue.put((word, correction))
        await asyncio.sleep(0)  # Simulate asynchronous processing

class AddToDictionaryDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add to Custom Dictionary")

        self.label = tk.Label(self, text="Enter word to add:")
        self.entry = tk.Entry(self)
        self.add_button = tk.Button(self, text="Add", command=self.add_word)
        
        self.label.pack(pady=10)
        self.entry.pack(pady=10)
        self.add_button.pack(pady=10)

    def add_word(self):
        word = self.entry.get().strip()
        if word:
            custom_dictionary.append(word)
            messagebox.showinfo("Success", f"{word} added to custom dictionary.")
            self.destroy()

class SpellCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spell Checker App")

        self.spell_checker = SpellChecker(dictionary)
        self.custom_dictionary = custom_dictionary

        self.create_widgets()

    def create_widgets(self):
        self.text_entry_label = tk.Label(self, text="Enter text:")
        self.text_entry = tk.Text(self, height=10, width=40)
        self.check_button = tk.Button(self, text="Check Spelling", command=self.check_spelling)
        self.add_to_dict_button = tk.Button(self, text="Add to Custom Dictionary", command=self.show_add_to_dict_dialog)

        self.text_entry_label.pack(pady=10)
        self.text_entry.pack(pady=10)
        self.check_button.pack(pady=10)
        self.add_to_dict_button.pack(pady=10)

    def check_spelling(self):
        text_to_check = self.text_entry.get("1.0", "end-1c").split()
        
        response_time_sync = measure_response_time(self.spell_checker, text_to_check)
        messagebox.showinfo("Response Time", f"Sync Response Time per 1000 words: {response_time_sync:.4f} seconds")

        response_time_async = self.measure_response_time_async(text_to_check)
        messagebox.showinfo("Response Time", f"Async Response Time per 1000 words: {response_time_async:.4f} seconds")

    async def async_spell_check(self, spell_checker, words):
        loop = asyncio.get_event_loop()
        result_queue = asyncio.Queue()
        tasks = [async_spell_check(spell_checker, chunk, result_queue) for chunk in chunks(words, 10)]

        await asyncio.gather(*tasks)
        loop.close()

        return result_queue

    def measure_response_time_async(self, words):
        loop = asyncio.get_event_loop()
        start_time = time.time()

        result_queue = loop.run_until_complete(self.async_spell_check(self.spell_checker, words))

        end_time = time.time()
        elapsed_time = end_time - start_time

        words_processed = len(words)
        response_time_per_1000_words = (elapsed_time / words_processed) * 1000

        return response_time_per_1000_words

    def show_add_to_dict_dialog(self):
        AddToDictionaryDialog(self)

def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

if __name__ == "__main__":
    dictionary = [
        "example", "spell", "checker", "optimize", "efficient", "advanced", "algorithm", "demonstration",
        "programming", "language", "development", "repository", "version", "control", "source", "code",
        "computer", "science", "machine", "learning", "artificial", "intelligence", "data", "analysis",
        "visualization", "network", "security", "encryption", "authentication", "authorization", "framework",
        "application", "interface", "interface", "module", "library", "database", "management", "system",
        "architecture", "design", "pattern", "object", "oriented", "paradigm", "function", "procedure",
        "iteration", "recursion", "debugging", "testing", "integration", "deployment", "virtualization",
        "containerization", "microservices", "cloud", "computing", "web", "development", "frontend", "backend",
        "full-stack", "responsive", "design", "user", "experience", "agile", "scrum", "kanban", "sprint",
        "continuous", "integration", "continuous", "delivery", "automation", "devops", "deployment",
        "monitoring", "scaling", "optimization", "performance", "security", "risk", "analysis", "vulnerability",
        "penetration", "testing", "ethical", "hacking", "firewall", "intrusion", "detection", "prevention",
        "incident", "response", "recovery", "compliance", "framework", "regulation", "standard", "protocol",
        "networking", "router", "switch", "firewall", "subnet", "DNS", "TCP", "IP", "HTTP", "HTTPS", "SSL",
        "cryptography", "public", "private", "key", "certificate", "hash", "encryption", "decryption", "symmetric",
        "asymmetric", "RSA", "AES", "DES", "SHA", "MD5", "SHA-256", "SHA-3", "quantum", "computing", "blockchain",
        "bitcoin", "ethereum", "smart", "contract", "cryptocurrency", "token", "decentralized", "ledger",
        "consensus", "algorithm", "proof", "work", "proof", "stake", "delegated", "proof", "authority",
        "permissioned", "permissionless", "mining", "node", "wallet", "exchange", "ICO", "DAO", "whitepaper",
        "fintech", "regtech", "insurtech", "healthtech", "edtech", "govtech", "agtech", "biotech", "cleantech",
        "nanotech", "robotics", "autonomous", "vehicles", "virtual", "reality", "augmented", "reality", "gaming",
        "simulation", "cybersecurity", "privacy", "GDPR", "HIPAA", "CCPA", "SOX", "PCI", "DSS", "NIST", "ISO",
        "compliance", "risk", "management", "threat", "intelligence", "security", "operations", "SOC", "SIEM",
        "firewall", "IDS", "IPS", "VPN", "endpoint", "protection", "authentication", "authorization", "biometrics",
        "multifactor", "authentication", "security", "awareness", "training", "phishing", "malware", "ransomware",
        "zero-day", "exploit", "vulnerability", "patch", "security", "assessment", "pentest", "red", "team", "blue",
        "team", "purple", "team", "CISO", "security", "officer", "security", "analyst", "security", "engineer", "security",
        "consultant", "security", "architect", "security", "researcher", "security", "auditor", "incident", "responder",
        "forensics", "encryption", "cryptanalysis", "steganography", "homomorphic", "encryption", "privacy", "preserving",
        "cryptography", "security", "by", "design", "threat", "modeling", "secure", "SDLC", "OWASP", "top", "10", "vulnerabilities",
        "cross-site", "scripting", "SQL", "injection", "cross-site", "request", "forgery", "insecure", "direct", "object", "references",
        "security", "misconfiguration", "broken", "authentication", "session", "management", "security", "testing", "tools",
        "Burp", "Suite", "Nmap", "Wireshark", "Metasploit", "Aircrack-ng", "Hashcat", "John", "the", "Ripper", "OSINT", "maltego",
        "Shodan", "social", "engineering", "phishing", "spear", "phishing", "ransomware", "WannaCry", "NotPetya", "CryptoLocker",
        "Spyware", "Adware", "Trojan", "Horse", "Backdoor", "Rootkit", "Botnet", "DDoS", "IoT", "exploitation", "vulnerability",
        "management", "threat", "modeling", "secure", "SDLC", "ISO", "27001", "27002", "27005", "NIST", "SP", "800-53", "HIPAA",
        "HITECH", "Act", "FISMA", "PCI", "DSS", "SOC", "CMMI", "ITIL", "COBIT", "GDPR", "BYOD", "VPN", "MFA", "DNS", "HTTP", "HTTPS"
    ]

    custom_dictionary=[]

    app = SpellCheckerApp()
    app.mainloop()
