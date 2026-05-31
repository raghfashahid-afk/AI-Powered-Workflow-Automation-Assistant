import re

# Deadline keywords to look for
DEADLINE_PATTERNS = [
    r'(by|before|due|deadline|until|no later than)\s+([a-zA-Z]+\s+\d{1,2}|\d{1,2}\s+[a-zA-Z]+|\w+day|tomorrow|tonight|today)',
    r'(due|deadline)\s*:\s*([^\n,]+)',
    r'(submit|complete|finish|send|reply|respond)\s+.{0,30}(by|before|until)\s+([^\n,\.]+)',
]

# Task action keywords
TASK_KEYWORDS = [
    "submit", "complete", "finish", "send", "reply", "respond",
    "review", "approve", "sign", "attend", "join", "schedule",
    "prepare", "update", "confirm", "provide", "share", "upload",
    "download", "check", "verify", "fix", "resolve", "follow up"
]

PRIORITY_KEYWORDS = {
    "urgent":   ["urgent", "asap", "immediately", "critical", "emergency"],
    "high":     ["important", "priority", "deadline today", "due today"],
    "normal":   ["please", "kindly", "when possible"],
    "low":      ["whenever", "no rush", "low priority", "optional"]
}


def extract_deadline(text: str) -> str:
    """
    Extract deadline from email text using regex.
    """
    text_lower = text.lower()
    for pattern in DEADLINE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(0).strip()
    return None


def extract_priority(text: str) -> str:
    """
    Determine priority based on keywords.
    """
    text_lower = text.lower()
    for priority, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return priority
    return "normal"


def extract_tasks_from_email(email_text: str, email_subject: str = "") -> list:
    """
    Extract tasks from email body and subject.
    Returns list of task dicts.
    """
    tasks = []
    combined = f"{email_subject} {email_text}"
    sentences = re.split(r'[.!?\n]', combined)

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 10:
            continue

        sentence_lower = sentence.lower()

        # Check if sentence contains a task keyword
        for keyword in TASK_KEYWORDS:
            if keyword in sentence_lower:
                deadline = extract_deadline(sentence)
                priority = extract_priority(sentence)

                tasks.append({
                    "title":    sentence[:200],   # limit length
                    "deadline": deadline,
                    "priority": priority,
                    "status":   "pending"
                })
                break   # one task per sentence

    return tasks