def Fun(webpage, topic_id):
    base_url = "https://www.shaalaa.com" 
    #webpage = input("Enter the URL: ")
    #topic_id = input("Enter the topic ID: ")
    import requests
    get_result = requests.get(webpage, verify=False)
    html = get_result.text #step 1: html page fetched from the web
    html = html.replace("<br />", "\n")

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    answer_links = []
    links = soup.find_all("a", {"class": "view_solution"})
    for link in links:
        full_link = base_url + link['href']
        answer_links.append(full_link) #step 3: all solution links appended to answer_links list

    answer_types = []
    for answer_link in answer_links:
        ansRequest = requests.get(answer_link, verify=False)
        ansHtml = ansRequest.text
        ansSoup = BeautifulSoup(ansHtml, 'html.parser')
        qtype_div = ansSoup.find("div", {"class": "qbq_q_type"})
        qtype = qtype_div.text
        answer_types.append(qtype)
        #qtype could be 
        # MCQ
        # Fill in the Blanks, 
        # Short Note, 
        # Match the Columns,
        # Diagram,
        # Distinguish Between,
        # Sum,
        # One Line Answer,
        # Answer in Brief,
        # Chart
        # ...
    answer_count = len(answer_types)
    all_questions = []
    for _ in range(answer_count):
        all_questions.append(None)

    for i in range(answer_count):
        # # print(i)
        if (answer_types[i]=="Fill in the Blanks" or answer_types[i]=="Short Note" or answer_types[i]=="Diagram" or answer_types[i]=="Distinguish Between" or answer_types[i]=="Sum" or answer_types[i]=="One Line Answer" or answer_types[i]=="Answer in Brief"):
        #simple question statement, all enclosed in html_text div
            # # print(answer_types[i])
            html_wraps = soup.find_all("div", {"class": "html_wrap"})
            question_paragraphs = html_wraps[i].find("div", {"class": "html_text"}).find_all("p")
            question_statement = ""
            for question_paragraph in question_paragraphs:
                question_statement = question_statement + question_paragraph.text + "\n"
                all_questions[i] = question_statement
            
        elif answer_types[i]=="MCQ":
            #list type question statement
            html_wraps = soup.find_all("div", {"class": "html_wrap"})
            question_paragraphs = html_wraps[i].find("div", {"class": "html_text"}).find_all("p")
            question_statement = ""
            for question_paragraph in question_paragraphs:
                question_statement = question_statement + question_paragraph.text + "\n"
            option_list = html_wraps[i].find("ul", {"class": "qbq_items"}).find_all("li")
            options = []
            for option in option_list:
                options.append(option.text)
            all_questions[i] = [question_statement, options]
            # # print(answer_types[i])
        elif answer_types[i]=="Match the Columns":
            #table associated with the question
            # # print(answer_types[i])
            html_wraps = soup.find_all("div", {"class": "html_wrap"})
            question_paragraphs = html_wraps[i].find("div", {"class": "html_text"}).find_all("p")
            question_statement = ""
            for question_paragraph in question_paragraphs:
                question_statement = question_statement + question_paragraph.text + "\n"
            table_rows = html_wraps[i].find("div", {"class": "html_text"}).find("tbody").find_all("tr")
            col1 = []
            col2 = []
            for row in table_rows:
                col1.append(row.find_all("td")[0].text)
                col2.append(row.find_all("td")[1].text)
        # table = [col1, col2]
                table = []
                for k in range(len(col1)):
                    table.append([col1[k], col2[k]])
        #
            all_questions[i] = [question_statement, table]
        elif answer_types[i]=="Chart" or answer_types[i]=="Diagram":
            # # print(answer_types[i])
            all_questions[i] = "Chart/Diagram type question"
    all_answers = []
    for _ in range(answer_count):
        all_answers.append(None)

    for i in range(answer_count):
        ans_html = requests.get(answer_links[i], verify=False).text
        ans_html = ans_html.replace("<br />", "\n")
        ans_soup = BeautifulSoup(ans_html, 'html.parser')
        if(answer_types[i]=="MCQ"):
            ans = ans_soup.find("ul", {"class": "qbq_items"}).find("li", {"class": "question_item_answer"}).text
            all_answers[i] = ans
            # # print(all_answers[i])
        elif(answer_types[i]=="Match the Columns"):
            ans_rows = ans_soup.find("div", {"id": "answer1"}).find("table").find("tbody").find_all("tr")
            col1 = []
            col2 = []
            for row in ans_rows:
                anspairs = row.find_all("td")
                col1.append(anspairs[0].text)
                col2.append(anspairs[1].text)
            table = []
            for k in range(len(col1)):
                table.append([col1[k], col2[k]])
            all_answers[i] = table
            # # print(all_answers[i])
        elif(answer_types[i]=="Fill in the Blanks"):
            blanks = ans_soup.find("div", {"id": "answer1"}).find_all("strong")
            ans = []
            for blank in blanks:
                ans.append(blank.text)
            all_answers[i] = ans
        else:
            ans = ans_soup.find("div", {"id": "answer1"}).text
            all_answers[i] = ans


    counter = 1
    output = "<table id='excel-table' border='1px'><thead><th>TopicID</th><th>Difficulty Level</th><th>QuestionID</th><th>Question</th><th>Answer</th></thead><tbody>"
    for i in range(len(all_questions)):
        if answer_types[i]=="MCQ":
            # print("Q %s: %s" %(i+1, all_questions[i][0]))
            #for option in all_questions[i][1]:
                # print(option)
            # print("Ans: ")
            # print(all_answers[i])
            just_the_question = all_questions[i][0]
            output += "<tr><td>"+str(topic_id)+"</td><td>"+str(counter)+"</td><td>"+str(topic_id)+"_"+str(counter).zfill(3)+"</td><td>"+just_the_question+"</td><td>"+all_answers[i]+"</td></tr>"
            counter += 1
        elif answer_types[i]=="Match the Columns":
            # print("Q %s: %s" %(i+1, all_questions[i][0]))
            # table = all_questions[i][1]
            # for x in range(len(table)): #range starts from 1 because the first row contains table headers
            #     if(table[x][0]!='A'):
                    # print(table[x][0]+"   "+table[x][1])
            # print("Ans: ")
            # print(all_answers[i])
            table = all_questions[i]
            ans_table = all_answers[i]
            for x in range(len(ans_table)):
                if(ans_table[x][0][0]!="A"):
                    output += "<tr><td>"+str(topic_id)+"</td><td>"+str(counter)+"</td><td>"+str(topic_id)+"_"+str(counter).zfill(3)+"</td><td>Find my partner: "+ans_table[x][0]+"</td><td>"+ans_table[x][1]+"</td></tr>"
                    counter += 1
        elif answer_types[i]=="Chart" or answer_types[i]=="Diagram" or answer_types[i]=="Distinguish Between":
            a = 0
            # print("Images not rendered\n")
        elif answer_types[i]=="Fill in the Blanks":
            # print("Q %s: %s" %(i+1, all_questions[i]))
            # print("Ans: ")
            # print(all_answers[i])
            blanks = ""
            for x in range(len(all_answers[i])):
                if(x<len(all_answers[i])-1):
                    blanks = blanks + all_answers[i][x] + ","
                else:
                    blanks = blanks + all_answers[i][x]
            output += "<tr><td>"+str(topic_id)+"</td><td>"+str(counter)+"</td><td>"+str(topic_id)+"_"+str(counter).zfill(3)+"</td><td>"+all_questions[i]+"</td><td>"+blanks+"</td></tr>"
            counter += 1
        else:
            # print("Q %s: %s" %(i+1, all_questions[i]))
            # print("Ans: ")
            # print(all_answers[i])
            output += "<tr><td>"+str(topic_id)+"</td><td>"+str(counter)+"</td><td>"+str(topic_id)+"_"+str(counter).zfill(3)+"</td><td>"+all_questions[i]+"</td><td>"+all_answers[i]+"</td></tr>"
            counter += 1

    output += "</tbody></table>"

    return output
            

        
    # question_count = len(all_questions)
    # # print("Count: %s" %(question_count)) #prints the question count
