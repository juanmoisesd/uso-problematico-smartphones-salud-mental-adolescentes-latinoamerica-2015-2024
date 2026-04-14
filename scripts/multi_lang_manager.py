import os

# Comprehensive Metadata for the Global Academic Collection (29 languages)
# Format: {lang_code: {cap_num: {title: str, abstract: str}}}

global_metadata = {
    "de": { # German
        "cap1": {"title": "Der Zahleninstinkt: Phylogenetische und ontogenetische Grundlagen der numerischen Kognition", "abstract": "Die Fähigkeit, numerische Mengen wahrzunehmen und zu manipulieren, ist kein rein kulturelles Konstrukt, sondern wurzelt in einem evolutionär alten 'Zahlensinn'."},
        "cap2": {"title": "Die Geographie der Berechnung: Kartierung der funktionellen Neuroanatomie der mathematischen Verarbeitung", "abstract": "Die menschliche Fähigkeit zum mathematischen Denken wird durch ein komplexes und verteiltes Netzwerk von Gehirnregionen unterstützt."},
        "cap3": {"title": "Von Bauklötzen zu Gleichungen: Die Neurowissenschaft des mathematischen Lernens in der Kindheit", "abstract": "Der entwicklungsbedingte Übergang von der Wahrnehmung konkreter physikalischer Objekte zur Konzeptualisierung abstrakter mathematischer Gleichungen."},
        "cap4": {"title": "Das zerebrale Duell: Schnelle Intuition versus analytische Logik im mathematischen Denken", "abstract": "Mathematisches Denken ist kein monolithischer Prozess, sondern das Ergebnis eines dynamischen Zusammenspiels zwischen zwei kognitiven Systemen."},
        "cap5": {"title": "Gedächtnis-Abkürzungen: Wie das Gehirn die mathematische Berechnung durch synaptische Plastizität automatisiert", "abstract": "Die Beherrschung komplexer Mathematik hängt maßgeblich von der Automatisierung grundlegender numerischer Fakten und Verfahren ab."},
        "cap6": {"title": "Die Amygdala und die numerische Panik: Die Neurobiologie der Mathematikangst verstehen", "abstract": "Mathematikangst ist eine schwächende affektiv-kognitive Störung, die durch Gefühle von Spannung und Besorgnis gekennzeichnet ist."},
        "cap7": {"title": "Das getrennte Gehirn: Neurobiologische Einblicke in die Entwicklungsdiskalkulie", "abstract": "Die Entwicklungsdiskalkulie ist eine spezifische Lernstörung, die durch eine anhaltende Schwierigkeit beim Verständnis und Manipulieren von Zahlen gekennzeichnet ist."},
        "cap8": {"title": "Das mentale Fitnessstudio: Neuroplastizität und Strategien zur Stärkung des logischen Gehirns", "abstract": "Das menschliche Gehirn zeichnet sich durch eine außergewöhnliche Fähigkeit zur strukturellen und funktionellen Reorganisation während des gesamten Lebens aus."},
        "cap9": {"title": "Anatomie eines Genies: Neurobiologische Korrelate außergewöhnlicher mathematischer Begabung", "abstract": "Die Untersuchung mathematisch begabter Personen bietet eine einzigartige Gelegenheit, die oberen Grenzen des menschlichen kognitiven Potenzials zu erforschen."},
        "cap10": {"title": "Die neuronale Symphonie: Warum Mathematik die verborgene Sprache des Gehirns ist", "abstract": "Mathematik wird oft als kulturelle Erfindung betrachtet, doch ihre bemerkenswerte Wirksamkeit bei der Beschreibung der physischen Welt deutet auf eine tiefere Verbindung hin."}
    },
    "zh-Hant": { # Traditional Chinese
        "cap1": {"title": "數字本能：數字認知的系統發育與個體發育基礎", "abstract": "感知和操作數字數量的能力並非純粹的文化建構，而是根植於進化上古老的「數字感」。"},
        "cap2": {"title": "計算地理學：繪製數學處理的功能神經解剖圖", "abstract": "人類的數學推理能力由一個複雜且分佈的神經網絡支持。"},
        "cap3": {"title": "從積木到方程：兒童數學學習的神經科學", "abstract": "從感知具體物理對象到概念化抽象數學方程的發展過渡。"},
        "cap4": {"title": "大腦對決：數學推理中快速直覺與分析邏輯的對抗", "abstract": "數學推理不是一個單一的過程，而是兩個認知系統之間動態相互作用的結果。"},
        "cap5": {"title": "記憶捷徑：大腦如何通過突觸可塑性自動化數學計算", "abstract": "對複雜數學的掌握在很大程度上取決於基本數字事實和程序的自動化。"},
        "cap6": {"title": "杏仁核與數字恐慌：理解數學焦慮的神經生物學", "abstract": "數學焦慮是一種使人衰弱的情感認知障礙，其特徵是緊張和憂慮感。"},
        "cap7": {"title": "斷開連接的大腦：發育性計算障礙的神經生物學見解", "abstract": "發育性計算障礙是一種特定的學習障礙，其特徵是理解和操作數字存在持久困難。"},
        "cap8": {"title": "大腦健身房：神經可塑性與增強邏輯大腦的策略", "abstract": "人類大腦的特點是在整個生命過程中具有非凡的結構和功能重組能力。"},
        "cap9": {"title": "天才的解剖：非凡數學才能的神經生物學相關性", "abstract": "對具有數學天賦的個體的研究為探索人類認知潛力的上限提供了獨特的機會。"},
        "cap10": {"title": "神經交響曲：為什麼數學是大腦的隱藏語言", "abstract": "數學通常被視為一種文化發明，但它在描述物理世界方面的顯著有效性表明了兩者之間存在深層聯繫。"}
    },
    "ar": { # Arabic
        "cap1": {"title": "غريزة الأرقام: الأسس التطورية والنمائية للمعرفة العددية", "abstract": "القدرة على إدراك ومعالجة الكميات العددية ليست مجرد بناء ثقافي بحت، بل هي متجذرة في 'حس عددي' قديم تطورياً."},
        "cap2": {"title": "جغرافيا الحساب: رسم خرائط التشريح العصبي الوظيفي للمعالجة الرياضية", "abstract": "القدرة البشرية على الاستدلال الرياضي مدعومة بشبكة معقدة وموزعة من مناطق الدماغ."},
        "cap3": {"title": "من المكعبات إلى المعادلات: علم الأعصاب لتعلم الرياضيات في الطفولة", "abstract": "الانتقال النمائي من إدراك الأشياء المادية الملموسة إلى تصور المعادلات الرياضية المجردة."},
        "cap4": {"title": "المبارزة الدماغية: الحدس السريع مقابل المنطق التحليلي في الاستدلال الرياضي", "abstract": "الاستدلال الرياضي ليس عملية متجانسة، بل هو نتيجة تفاعل ديناميكي بين نظامين معرفيين."},
        "cap5": {"title": "اختصارات الذاكرة: كيف يقوم الدماغ بأتمتة الحساب الرياضي من خلال اللدونة التشابكية", "abstract": "يعتمد إتقان الرياضيات المعقدة بشكل كبير على أتمتة الحقائق والإجراءات العددية الأساسية."},
        "cap6": {"title": "اللوزة الدماغية والذعر العددي: فهم البيولوجيا العصبية لقلق الرياضيات", "abstract": "قلق الرياضيات هو اضطراب عاطفي معرفي منهك يتميز بمشاعر التوتر والوجل."},
        "cap7": {"title": "الدماغ المنفصل: رؤى عصبية حيوية في عسر الحساب النمائي", "abstract": "عسر الحساب النمائي هو اضطراب تعلم محدد يتميز بصعوبة مستمرة في فهم ومعالجة الأرقام."},
        "cap8": {"title": "الصالة الرياضية العقلية: اللدونة العصبية واستراتيجيات تعزيز الدماغ المنطقي", "abstract": "يتميز الدماغ البشري بقدرة غير عادية على إعادة التنظيم الهيكلي والوظيفي طوال الحياة."},
        "cap9": {"title": "تشريح العبقري: الارتباطات البيولوجية العصبية للموهبة الرياضية الاستثنائية", "abstract": "توفر دراسة الأفراد الموهوبين رياضياً فرصة فريدة لاستكشاف الحدود القصوى للإمكانات المعرفية البشرية."},
        "cap10": {"title": "السيمفونية العصبية: لماذا تعتبر الرياضيات اللغة الخفية للدماغ", "abstract": "غالباً ما تُعتبر الرياضيات اختراعاً ثقافياً، ومع ذلك فإن فعاليتها الملحوظة في وصف العالم المادي تشير إلى وجود رابط عميق."}
    }
    # (Full 29-language set will be implemented in the execution phase)
}

def get_translated_headings(lang_code):
    headings = {
        "de": ["Zusammenfassung", "Schlüsselwörter", "Einleitung", "Methode", "Ergebnisse", "Diskussion", "Schlussfolgerungen", "Referenzen"],
        "zh-Hant": ["摘要", "關鍵詞", "引言", "方法", "結果", "討論", "結論", "參考文獻"],
        "ar": ["ملخص", "الكلمات المفتاحية", "مقدمة", "المنهجية", "النتائج", "المناقشة", "الاستنتاجات", "المراجع"],
        "en": ["Abstract", "Keywords", "Introduction", "Method", "Results", "Discussion", "Conclusions", "References"]
    }
    return headings.get(lang_code, headings["en"])

def generate_multi_lang_markdown(lang_code, cap_num, source_en_path):
    # This logic will be used to generate the high-quality multi-language .md files
    # By combining the translated metadata and headings with the English source text (for rigor)
    pass
