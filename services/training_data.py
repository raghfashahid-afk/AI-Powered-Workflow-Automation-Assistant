# Labeled training data for our ML model
# Format: (text, label)

TRAINING_DATA = [
    # URGENT
    ("urgent action required immediately deadline expires today", "urgent"),
    ("critical alert your account will be suspended respond now", "urgent"),
    ("immediate response needed time sensitive matter asap", "urgent"),
    ("warning last chance to respond before deadline critical", "urgent"),
    ("action required urgent security alert verify immediately", "urgent"),
    ("your account expires today urgent action needed now", "urgent"),
    ("final notice deadline tomorrow respond immediately urgent", "urgent"),
    ("important alert action required within 24 hours critical", "urgent"),
    ("emergency notification respond asap time sensitive warning", "urgent"),
    ("last warning account suspension imminent act now urgent", "urgent"),

    # SPAM
    ("you won a prize claim your free gift now limited offer", "spam"),
    ("congratulations winner free money lottery claim reward", "spam"),
    ("buy now discount deal offer click here limited time cheap", "spam"),
    ("make money fast earn cash online investment opportunity", "spam"),
    ("free gift card winner selected claim prize now", "spam"),
    ("hot deal discount buy cheap offer sale click now", "spam"),
    ("you are selected winner claim free reward today", "spam"),
    ("earn money from home easy income investment opportunity", "spam"),
    ("free trial no credit card required buy now limited", "spam"),
    ("casino online gambling earn win free bonus claim now", "spam"),

    # NEWSLETTER
    ("weekly newsletter digest edition monthly update subscribers", "newsletter"),
    ("unsubscribe mailing list newsletter weekly digest edition", "newsletter"),
    ("monthly digest top stories newsletter edition update", "newsletter"),
    ("this week newsletter roundup edition subscribers update", "newsletter"),
    ("our latest newsletter campaign monthly edition announcement", "newsletter"),
    ("newsletter subscription weekly digest unsubscribe update", "newsletter"),
    ("community update newsletter digest monthly edition news", "newsletter"),
    ("blog post weekly roundup newsletter digest mailing list", "newsletter"),
    ("latest edition newsletter update subscribers announcement", "newsletter"),
    ("unsubscribe newsletter monthly digest edition update list", "newsletter"),
    
    # SOCIAL
    ("linkedin connection request invitation network profile", "social"),
    ("facebook friend request tagged mentioned notification", "social"),
    ("github pull request mentioned issue comment notification", "social"),
    ("twitter follower mentioned liked retweeted notification", "social"),
    ("instagram liked your photo comment follower notification", "social"),
    ("linkedin job opportunity connection invitation network", "social"),
    ("someone commented on your post social media notification", "social"),
    ("new follower connection request social network profile", "social"),
    ("you were mentioned tagged social media notification alert", "social"),
    ("linkedin message connection invitation mutual network", "social"),

    # IMPORTANT
    ("invoice payment receipt order confirmation transaction", "important"),
    ("meeting appointment scheduled interview confirmation time", "important"),
    ("project proposal contract agreement signature required", "important"),
    ("password reset verification account security login", "important"),
    ("order shipped tracking number delivery confirmation", "important"),
    ("report submission deadline project update team meeting", "important"),
    ("payment confirmation receipt invoice order processing", "important"),
    ("security verification code account login confirmation", "important"),
    ("job interview confirmation appointment schedule time", "important"),
    ("contract proposal agreement review sign document", "important"),

    # GENERAL
    ("hello how are you doing today hope everything well", "general"),
    ("thank you for your message will get back to you soon", "general"),
    ("just checking in wanted to say hello hope you good", "general"),
    ("following up on our previous conversation let me know", "general"),
    ("sharing some thoughts wanted your feedback opinion", "general"),
    ("quick question regarding our discussion earlier today", "general"),
    ("forwarding this email for your information reference", "general"),
    ("please find attached document for your review thanks", "general"),
    ("reminder about our upcoming event hope to see you", "general"),
    ("introduction wanted to connect and share information", "general"),
]