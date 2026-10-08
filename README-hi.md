# dsh-sop-sync-check — कार्य-अनुदेश रजिस्टर तथा PFMEA / नियंत्रण योजना की संगति जाँच

`dsh-sop-sync-check` एक कार्य-अनुदेश रजिस्टर पढ़ता है — उत्पाद हेडर और प्रत्येक प्रक्रिया की एक पंक्ति — और उस रजिस्टर की उसके द्वारा उद्धृत PFMEA तथा नियंत्रण योजना के साथ यांत्रिक संगति जाँचता है: हर प्रक्रिया पंक्ति में प्रक्रिया-अनुदेश क्रमांक दर्ज है या नहीं, PFMEA या नियंत्रण योजना का उल्लेख है या नहीं, पंक्ति में उद्धृत संस्करण रजिस्टर में दर्ज वर्तमान संस्करण से मेल खाता है या नहीं, दर्ज किए गए पैरामीटर के साथ सह्यता (tolerance) दर्ज है या नहीं, कोई प्रक्रिया क्रमांक दोहराया नहीं गया है या नहीं, हेडर उत्पाद बताता है या नहीं, और संशोधन तिथि पढ़ी जा सकती है तथा जाँच-तिथि से बाद की नहीं है या नहीं। यह नहीं आँकता कि प्रक्रिया पैरामीटर सही हैं, नियंत्रण योजना सभी विफलता-प्रकारों को समेटती है, या PFMEA विश्लेषण पर्याप्त है; जो जाँच चल नहीं सकती वह चुपचाप पास होने के बजाय `skipped` में दर्ज होती है।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| किसी प्रक्रिया पंक्ति के 规程编号 कॉलम में प्रक्रिया-अनुदेश क्रमांक नहीं है। | `SS-001` उस पंक्ति को दर्ज करता है: नियम चाहता है कि जिस भी पंक्ति में यह कॉलम मौजूद है उसमें क्रमांक भरा हो, और यह केवल उपस्थिति देखता है — यह नहीं कि वह प्रक्रिया-अनुदेश उसी प्रक्रिया का सही अनुदेश है। यदि सामग्री में यह कॉलम ही न हो, तो नियम चुपचाप पास होने के बजाय बताता है कि वह लागू नहीं होता। |
| यह कार्य-अनुदेश किस PFMEA और किस नियंत्रण योजना का है, यह कहीं दर्ज नहीं है। | `SS-002` हर पंक्ति में PFMEA编号 और 控制计划编号 में से कम से कम एक भरा होने की अपेक्षा करता है। यह केवल देखता है कि कम से कम एक उद्धृत है — यह नहीं कि उद्धरण उपयुक्त है, और यह भी नहीं कि उसमें लिखा संस्करण वर्तमान है; वह तुलना `SS-003` करता है। |
| प्रक्रिया-अनुदेश में अब भी PFMEA का पिछला संस्करण उद्धृत है। क्या यह पकड़ में आता है? | हाँ। `SS-003` संस्करण अलग कॉलम से, या उद्धरण-पाठ के अंत में लगे संस्करण-चिह्न से लेता है (`PFMEA-2026-003 V2`); चिह्न के लिए `V`, `VER`, `REV`, `版本` या `版次` जैसा स्पष्ट संकेत ज़रूरी है, इसलिए दस्तावेज़ क्रमांक के अंत के अंकों को संस्करण नहीं मान लिया जाता। जिस उद्धरण का संस्करण-पाठ दस्तावेज़ के वर्तमान संस्करण से भिन्न है, वह पंक्ति दर्ज होती है, और यह केवल संस्करण-पाठ की तुलना करता है — यह नहीं तय करता कि उद्धरण किस संस्करण की ओर होना चाहिए। न संस्करण कॉलम हो न पढ़ने योग्य संस्करण-पाठ, तो यह नियम स्वयं को `skipped` में दर्ज करता है। |
| पैरामीटर कॉलम भरा है, पर 参数公差 कॉलम खाली है। | `SS-004` उस पंक्ति को दर्ज करता है, पर केवल तब जब पैरामीटर कॉलम भरा हो, इसलिए जिस प्रक्रिया में वास्तव में कोई पैरामीटर नहीं है वह पंक्ति दर्ज नहीं होती। यह देखता है कि सह्यता कॉलम भरा है, यह नहीं कि पैरामीटर और उसकी सह्यता उचित हैं। |
| एक ही प्रक्रिया क्रमांक दो पंक्तियों में आया है। | `SS-005` दोहराया गया 工序号 दर्ज करता है और बताता है कि वह पहली बार किस पंक्ति में आया; तुलना करते समय खाली स्थान छोड़ दिए जाते हैं। दोहराव का अर्थ आम तौर पर दोहरा पंजीकरण या क्रमांक की चूक है — कौन-सी पंक्ति सही है, यह मनुष्य का निर्णय रहता है। प्रक्रिया क्रमांक का कॉलम ही न हो तो नियम पास होने के बजाय बताता है कि वह लागू नहीं होता। |
| एक संशोधन तिथि `2026/3/8` लिखी है और एक पंक्ति में अगले महीने की तिथि है। | `SS-007` उस 修订日期 को दर्ज करता है जिसे वह तिथि के रूप में नहीं पढ़ सकता, और उस तिथि को भी जो जाँच-तिथि के बाद पड़ती है। यह देखता है कि तिथि पढ़ी जा सके और जाँच-तिथि के बाद न पड़े; यह नहीं आँकता कि संशोधन समय पर हुआ या नहीं। |

## यह किन मानकों पर आधारित है

यह नियम-पैक किसी सार्वजनिक मानक का उद्धरण नहीं देता: सत्यापन को IATF 16949 और ऑटोमोटिव कोर-टूल्स पुस्तिकाओं का शब्दशः खंड-पाठ नहीं मिला, इसलिए हर नियम का `basis` यही बात स्पष्ट लिखता है, सभी `derived-from-principle` हैं और कोई भी `warn` से ऊपर नहीं जाता। जाँचें जिन पर टिकती हैं वे हैं रजिस्टर का अपना लिखा क्रमांक और संस्करण — उसके कॉलम में लिखा प्रक्रिया-अनुदेश क्रमांक, PFMEA या नियंत्रण योजना के उद्धरण के साथ दर्ज संस्करण, पैरामीटर के पास लिखी सह्यता, संशोधन तिथि — और उनकी आपसी तुलना।

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| IATF 16949／汽车行业核心工具手册 | 现行版本与条号本次未核实 | SS-001, SS-002, SS-003, SS-004, SS-005, SS-006, SS-007 |

**Boundary:** this plugin checks a **作业规程台账** for mechanical consistency with its **PFMEA** and
**control plan** — that a number is recorded, that the PFMEA and control plan are cited, that the revision a
procedure cites matches the document's current revision, that a parameter has a tolerance, that process
numbers are unique, that the register names its product, and that revision dates parse. It does **not** judge
whether the process parameters are right, whether the control plan covers every failure mode, or whether the
PFMEA analysis is adequate. **Those are the process and quality engineers' judgements.**

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The regime lives in IATF 16949 and the automotive core-tools handbooks (APQP, PFMEA, control
> plan). The verification pass could not retrieve verbatim clause text from them, so rather than paraphrase a
> quotation the pack states the gap in the `excerpt` field itself and puts the honest reasoning in `note`.
> Every rule is therefore `warn` or `info`, and a test asserts that no rule claims a quotation it does not
> have. **When the texts are in hand, two things must be done: replace each `excerpt` with the real clause,
> and raise `kind` to `direct`.**
>
> `SS-003` is the one that earns its keep: **a procedure still citing the previous PFMEA revision** is the
> commonest and most dangerous way the three documents drift apart. It reads the revision either from a
> dedicated column or from a version marker at the tail of the reference text (`PFMEA-2026-003 V2`), and it
> needs an explicit cue — `V`, `VER`, `REV`, `版本`, `版次` — so that the trailing digits of a *document
> number* are never mistaken for a revision. With neither source available it reports itself in `skipped`.

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-sop-sync-check
dsh --profile <name> --dump-config | grep 'dsh-sop-sync-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/sop-sync-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-sop-sync-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-sop-sync-check contributors.
