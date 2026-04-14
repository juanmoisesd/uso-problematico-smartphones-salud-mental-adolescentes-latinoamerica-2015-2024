import json

# Standard headers for the 29 languages
headers_map = {
    "en": ["Abstract", "Introduction", "Method", "Results", "Discussion", "Conclusions", "References"],
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
    "sl": ["Povzetek", "Uvod", "Metoda", "Rezultati", "Razprava", "Zaključki", "Reference"],
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

# This meta-metadata will drive the generation of the 290 publications
full_collection_metadata = {}

# Basic Title templates for Cap 2 (as an example of orchestration logic)
cap2_titles = {
    "de": "Die Geographie der Berechnung",
    "zh-Hant": "計算地理學",
    "ar": "جغرافيا الحساب",
    # ...
}

with open("scripts/full_collection_metadata.json", "w", encoding="utf-8") as f:
    json.dump({"headers": headers_map}, f, ensure_ascii=False, indent=4)
