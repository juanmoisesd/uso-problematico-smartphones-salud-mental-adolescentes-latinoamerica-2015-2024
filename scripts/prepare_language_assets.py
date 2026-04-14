import json

# Comprehensive academic headers
headers_map = {
    "en": ["Abstract", "Introduction", "Method", "Results", "Discussion", "Conclusions", "References"],
    "es": ["Resumen", "Introducción", "Método", "Resultados", "Discusión", "Conclusiones", "Referencias"],
    "de": ["Zusammenfassung", "Einleitung", "Methode", "Ergebnisse", "Diskussion", "Schlussfolgerungen", "Referenzen"],
    "it": ["Abstract", "Introduzione", "Metodo", "Risultati", "Discussione", "Conclusioni", "Riferimenti"],
    "pt": ["Resumo", "Introdução", "Método", "Resultados", "Discussão", "Conclusões", "Referências"],
    "nl": ["Samenvatting", "Inleiding", "Methode", "Resultaten", "Discussie", "Conclusies", "Referenties"],
    "pl": ["Streszczenie", "Wstęp", "Metoda", "Wyniki", "Dyskusja", "Wnioski", "Referencje"],
    "sv": ["Sammanfattning", "Inledning", "Metod", "Resultat", "Diskussion", "Slutsatser", "Referenser"],
    "cs": ["Abstrakt", "Úvod", "Metoda", "Výsledky", "Diskuse", "Závěry", "Reference"],
    "fi": ["Tiivistelmä", "Johdanto", "Menetelmä", "Tulokset", "Pohdinta", "Johtopäätökset", "Viitteet"],
    "da": ["Abstrakt", "Indledning", "Metode", "Resultater", "Diskussion", "Konklusioner", "Referencer"],
    "el": ["Περίληψη", "Εισαγωγή", "Μέθοδος", "Αποτελέσματα", "Συζήτηση", "Συμπεράσματα", "Βιβλιογραφία"],
    "hu": ["Absztrakt", "Bevezetés", "Módszer", "Eredmények", "Diszkusszió", "Következtetések", "Referenciák"],
    "sk": ["Abstrakt", "Úvod", "Metóda", "Výsledky", "Diskusia", "Závery", "Referencie"],
    "bg": ["Резюме", "Въведение", "Метод", "Резултати", "Дискусия", "Заключения", "Източници"],
    "ro": ["Rezumat", "Introducere", "Metodă", "Rezultate", "Discuție", "Concluzii", "Referințe"],
    "hr": ["Sažetak", "Uvod", "Metoda", "Rezultati", "Rasprava", "Zaključci", "Reference"],
    "lt": ["Santrauka", "Įvadas", "Metodas", "Rezultatai", "Diskusija", "Išvados", "Literatūra"],
    "lv": ["Kopsavilkums", "Ievads", "Metode", "Rezultāti", "Diskusija", "Secinājumi", "Atsauces"],
    "et": ["Kokkuvõte", "Sissejuhatus", "Metoodika", "Tulemused", "Arutelu", "Järeldused", "Viited"],
    "sl": ["Povzetek", "Uvod", "Metoda", "Rezultati", "Razprava", "Zaključci", "Reference"],
    "mt": ["Astratt", "Introduzzjoni", "Metodu", "Riżultati", "Diskussjoni", "Konklużjonijiet", "Referenzi"],
    "ga": ["Achoimre", "Réamhrá", "Modh", "Torthaí", "Plé", "Conclúidí", "Tagairtí"],
    "hi": ["सारांश", "परिचय", "विधि", "परिणाम", "चर्चा", "निष्कर्ष", "संदर्भ"],
    "zh-Hant": ["摘要", "引言", "方法", "結果", "討論", "結論", "參考文獻"],
    "ko": ["초록", "서론", "방법", "결과", "고찰", "결론", "참고문헌"],
    "ms": ["Abstrak", "Pengenalan", "Kaedah", "Keputusan", "Perbincangan", "Kesimpulan", "Rujukan"],
    "id": ["Abstrak", "Pendahuluan", "Metode", "Hasil", "Diskusi", "Kesimpulan", "Referensi"],
    "ar": ["ملخص", "مقدمة", "المنهجية", "النتائج", "المناقشة", "الاستنتاجات", "المراجع"],
    "he": ["תקציר", "מבוא", "שיטה", "תוצאות", "דיון", "מסקנות", "ביבליוגרפיה"],
    "ja": ["要旨", "はじめに", "方法", "結果", "考察", "結論", "参考文献"]
}

# Localized titles for all chapters
chapter_titles = {
    "cap1": {"en": "The Number Instinct", "es": "El instinto numérico", "de": "Der Zahleninstinkt", "it": "L'istinto numerico", "ar": "غريزة الأرقام"},
    "cap2": {"en": "The Geography of Calculation", "es": "La geografía del cálculo", "de": "Die Geographie der Berechnung", "zh-Hant": "計算地理學"},
    "cap3": {"en": "From Blocks to Equations", "es": "De los bloques a las ecuaciones", "ko": "積木到方程"},
    "cap4": {"en": "The Cerebral Duel", "es": "El duelo cerebral", "ja": "大脳の対決"},
    "cap5": {"en": "Memory Shortcuts", "es": "El atajo de la memoria", "hi": "मेमोरी शॉर्टकट्स"},
    "cap6": {"en": "The Amygdala and Numerical Panic", "es": "La amígdala y el pánico a los números"},
    "cap7": {"en": "The Disconnected Brain", "es": "El cerebro desconectado", "pt": "O Cérebro Desconectado"},
    "cap8": {"en": "The Mental Gym", "es": "El gimnasio mental", "nl": "De Mentale Sportschool"},
    "cap9": {"en": "Anatomy of a Genius", "es": "Anatomía de un genio", "ru": "Анатомия гения"},
    "cap10": {"en": "The Neuronal Symphony", "es": "La sinfonía neuronal", "fr": "La symphonie neuronale"}
}

# Fill missing titles with EN base as fallback for global consistency
for cap in chapter_titles:
    base = chapter_titles[cap]["en"]
    for lang in headers_map:
        if lang not in chapter_titles[cap]:
            chapter_titles[cap][lang] = f"{base} ({lang})"

with open("scripts/language_assets.json", "w", encoding="utf-8") as f:
    json.dump({"headers": headers_map, "chapter_titles": chapter_titles}, f, ensure_ascii=False, indent=4)
