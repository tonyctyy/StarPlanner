import openai

# Example OpenAI Python library request
MODEL = "gpt-3.5-turbo"

def general_comment(comments):
   

    general_prompt = [{"role": "assistant", "content": "我是一名學業培導師，將會就一名同學的學習狀況進行分析，因此需要保持溫和的態度。"},
                       {"role": "user", "content": "接下來我將會提供同學的一些行爲或評語，請你幫我整合内容並重新寫成一段文字，描述同學的表現和行爲。"},
                       {"role": "user", "content": comments}]

# def social_style_general():
    # Define the conversation array with prompts for each step
def social_style_comment(scores, personalisation):
    social_style_general_prompt = [
        {"role": "assistant", "content": "我是一名學業培導師，將會就一名同學的待人處事風格結果分數進行分析，因此需要保持溫和的態度。\n\
而待人處事風格代表了在與人相處或對待事情時的傾向，分數低不代表能力較弱，可能只是比較注重其他層面的意向。\n\
而待人處事風格以兩個層面來引申4種風格。\
層面：\
1. 影響: 一個人有多大的意圖去改變他人的思想和行動\
2. 表達：一個人有多大的程度去向別人抒發他的感受\
結果：\
1. 影響低表達低: 分析型\
2. 影響高表達低: 推動型\
3. 影響低表達高: 友善型\
4. 影響高表達高: 表達型"},
        {"role": "assistant", "content": "在分析中將會根據待人處事風格的結果使用這些字詞，并且根據程度調整用語。\
優點：\
{分析型: [準確, 小心、謹慎, 有所保留, 邏輯性的, 分析性的],\
推動型: [清晰, 有效率, 決斷, 直接, 果斷],\
友善型: [親切, 接納, 有耐性的, 合作, 友善],\
表達型: [具活力的, 具創意的, 開明, 樂觀, 反應快]}\
弱項：\
{分析型: [頑固、死板, 苛求挑剔, 引經據典、賣弄學問, 不訴諸感情],\
推動型: [專制獨裁, 好批評, 諸多要求, 對人的感覺遲鈍, 一言堂],\
友善型: [懦弱, 膽小, 猶豫不決,浪費時間, 欠缺目標],\
表達型: [膚淺, 浮誇、言過其實, 虎頭蛇尾, 沒有跟進, 自負]}"},
        {"role": "assistant", "content": "同學有主要和次要的待人處事風格(如兩個風格相等，則是有兩個主要風格)，請在分析時考慮兩個風格。"},
        {"role": "assistant", "content": "以下是其中一位同學的例子：\
友善推動型 (中高友善，中高推動) \n 分析型: 20, 友善型: 35, 表達型: 10, 推動型: 35\n\
内容：\n\
友善表達型（高度友善，中等表達）\n\
    陳同學具備了友善型的親切和合作態度，以及推動型的果斷和有效率。這種風格的人通常能夠平易近人地與他人交流，並表現出對他人的尊重和善意。同時 ，他也非常目標導向，能夠迅速做出決策和推動事情的進展。\
陳同學的親切和合作態度使他在團隊合作中可能表現出色，能夠與他人建立良好的夥伴關係。他的果斷和有效率也能夠幫助他在短時間內完成任務和 實現目標。\n\
    然而，也需要注意一些弱項。陳同學可能在和別人溝通時過於友善，有時候可能欠缺一些堅定和直接性。在工作或團隊項目中，他可能需要更多的明確表達自己 的需求和要求的能力。\
同時，他在工作時可能會過於關注人際關係，有時可能忽略了一些細節或缺乏一定的批評能力。\n\
    作為建議，陳同學可以更加主動地提出自己的想法和觀點，不要過於含蓄或畏於直接表達。同時，考慮到他友好待人的本性，他可以培養一些批評和建設性反饋 的能力，以幫助他更全面地理解問題和改進工作。"}, 
        {"role": "user", "content": "請為"+ scores[0] +"的待人處事風格測驗進行分析，並跟據例子以數句句子為以下分數提供評語和建議。\n" + scores[1] + "\n 分析型: " + str(scores[2]) + ", 友善型: " + str(scores[3]) + ", 表達型: " + str(scores[4]) + ", 推動型: " + str(scores[5])},
        {"role": "user", "content": "以下是關於"+ scores[0] +"的個人化評語和建議" + personalisation + "請將文章與上述個人化評論結合"},
        {"role": "assistant", "content": "請把評論拆分為以下4部分，同時保留同學的社交風格類型標題。\n" + scores[1] + "\n 特質分析 \n 注意事項 \n 建議 \n 總結"}]
    
    response = openai.ChatCompletion.create(
        model=MODEL, 
        messages=social_style_general_prompt,
        temperature=1.1,
        n=1
    )
    return response


skills_and_competencies_dict = {
    "critical_thinking": ["批判性思維", ["表現出知識正直、公平和開放的思想", "綜合思想和資訊，以發現或擴展理解", "反思和評估思想、信仰或行為背後的推理", "應用合理的方法或相關準則來概念化、分析或做出判斷", "質疑和分析證據、斷言或假設"], 
                            "能力描述：涉及使用推理和準則來概念化、評估或綜合想法。學生反思自己的想法以改進它。他們挑戰思想、信仰或行動背後的假設。學生重視誠實、公平和開放的思想。\n\
能力指標：\n 1. 表現出知識正直、公平和開放的思想\n 2. 綜合思想和資訊，以發現或擴展理解\n 3. 反思和評估思想、信仰或行為背後的推理\n 4. 應用合理的方法或相關準則來概念化、分析或做出判斷\n 5. 質疑和分析證據、斷言或假設\n\
可見行為：\n 1. \n • 我抱持公平的心態，在做出判斷或決定時直面自己的偏見。\n • 我對自己的思想或行為的影響承擔道德責任。\n 2.\n • 我彙集相關信息和觀點，為思想、行動或信仰提供資訊。\n • 我透過情況或信息進行推斷或預測。\n\
3.\n • 我能解釋我的思考、想法或行動。\n • 我考慮背景或結合不同的觀點來評估想法或行動。\n 4.\n • 我使用準則來組織、分類或評估資訊。\n • 我遵循邏輯程序得出結論。\n 5. \n • 我檢查聲明的可靠性、偏見或可信度。\n • 我評估證據的相關性、準確性或精確性。\n\
典型行爲及其評分：\n 1.\n 分數 3：該學生偶爾挑戰其偏見，但在認識其對思考的影響方面仍有待提高。\n 分數 6：該學生通過挑戰偏見並積極尋求不同觀點，展現了公正、開放心態和智慧誠實。\n 2.\n 分數 3：該學生偶爾整合相關信息和觀點，但可能難以連貫且具有深度地進行整合。\n 分數 6：該學生一貫地綜合相關信息和觀點，有效地整合來源並進行有深度的推斷或預測。\n\
3.\n 分數 3：該學生有時解釋他們的推理，但可能缺乏深度，未能考慮更廣泛的背景或替代觀點，當反思並評估思想、信念或行動時。\n 分數 6：該學生一貫地解釋他們的推理，考慮背景，並納入不同觀點，當反思並評估思想、信念或行動時。\n 4.\n 分數 3：該學生有時運用標準，但在概念化、分析或做出判斷的方法上可能缺乏一致性和深度。\n 分數 6：該學生一貫地運用相關標準，遵循邏輯程序，在概念化、分析或做出判斷時展示出強大的分析思維能力。\n\
5. \n 分數 3：該學生偶爾檢查主張的可靠性、偏見或可信度，但在分析上可能缺乏深度。他們可能難以始終評估證據的相關性、精確性或準確性。\n 分數 6：該學生一貫地質疑和分析證據、主張或假設，考慮到可靠性、偏見、可信度、相關性、精確性和準確性等因素。"],
    "Problem_Solving": "解決問題",
    "Managing_Information": "管理資訊",
    "Creativity_and_Innovation": "創意與創新",
    "Communication": "表達與溝通",
    "Collaboration": "團隊合作",
    "Culttural_and_Global_Citizenship": "文化和全球公民意識",
    "Personal_growth_and_well-being": "個人成長"
}
def skills_and_competencies_comments(instruction, scores, behaviors):
    score = ""
    behavior = ""
    n_behavior = 1
    for indicator in instruction[1]:
        score += indicator + ": " + str(scores[instruction[1].index(indicator)+1]) + "\n"
    for b in behaviors:
        behavior += str(n_behavior) + "." + b + "\n"
        n_behavior += 1
    skills_and_competencies_prompt = [
        {"role": "assistant", "content": "你是一名學業培導師，接下來將會就一位同學的學生能力模型進行分析並提供評語和注意事項。\
學生能力模型整合了學生在學習和與人相處時使用8種不同能力的習慣和傾向，評分標準為(1-6分，1分代表學生從不使用該能力，6分代表總是使用該能力)，分數的高低不代表能力的優劣。\
每項能力由5-6個能力指標組合而成，能力指標提供了更完整和詳細的評分角度，可見行爲說明了能力指標在不同情況下可能出現的方式，典型行爲及其評分則提供了不同分數可參考的評語。\
在提供評語時不要强調分數，而是提出分數可能代表的表現和行爲。提供評語時亦不用説明就那個能力指標而言，而是把能力指標融入句子中表達。請把同學的實際行爲融入評語和注意事項的描述中。"},
        {"role": "assistant", "content": "以下是" + instruction[0] + "評分標準的細項：\n" + instruction[2]},
        {"role": "user", "content": "請為"+ scores[0] +"進行分析並提供評語和注意事項：1. 評語(請整合成一段):\n 2. 注意事項(請整合成一段):\n\
以下是"+ scores[0] +"不同能力指標的得分和他的實際行爲，請嘗試在描述中融入他的實際行爲：\n" + score + "實際行爲：\n" + behavior}]
    
    response = openai.ChatCompletion.create(
        model=MODEL,  # Use the appropriate engine
        messages=skills_and_competencies_prompt,
        temperature=1.1,
        n=1
    )
    return response




# Social Style Input
scores = ['蘇同學','表達分析型(高度表達，中度推動)', 25, 15, 45, 15]
personalisation = "特質分析：蘇同學在待人處事上展現了表達型和分析型的優點，而分析型的處事風格也彌補了表達型處事風格中可能缺乏事實和實際性的缺點。\n\
            注意事項：蘇同學有時候過於追求他人的肯定和贊賞，這樣的追求可能使他自身承受過多壓力。因此，蘇同學應該適當地降低對自己的要求，以減輕壓力的負擔。\
                同時，蘇同學在表達自己觀點和意見時，有時可能忽略了他人的感受和想法。為了改善這一點，他可以更加注重感受的重要性，並在表達意見時傾聽他人的觀點。\n"
# social_style_response = social_style_comment(scores, personalisation)

# Skills & Competencies Input
skills_and_competencies_instruction = skills_and_competencies_dict["critical_thinking"]
skills_and_competencies_scores = ["錢同學" ,3, 3, 4, 4, 3]
skills_and_competencies_behavior = ["選擇口腔科時能考慮未來的前景和自身的興趣，並能和想近的學科作出比較。", "作議論文時每次都能做詳細資料搜集，文章邏輯清晰章邏輯清晰。"]
skills_and_competencies_response = skills_and_competencies_comments(skills_and_competencies_instruction,skills_and_competencies_scores, skills_and_competencies_behavior)

# Print the finalized comment
print(skills_and_competencies_response)
for message in skills_and_competencies_response.choices:
    print("Generated Comment:")
    print(message.message["content"])