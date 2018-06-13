import re
import json


w = open("dic.txt", "w")

problem = []

index = 1
with open("fit.txt", "r") as f:
    dic_list = []
    dic = {}
    pivot = None
    for line in f.readlines():
        new_line = re.sub(r'(?is)\[\[',' ',line)
        new_line = re.sub(r'(?is)\]\]',' ',new_line)
        new_line = re.sub(r'\]', ' ', new_line)
        new_line = re.sub(r'\[', ' ', new_line)
        #new_line = re.sub(r'", "', ' ', new_line)
        new_line = re.sub(r'" ,  "',',', new_line)
        #new_line = re.sub(r'\{\{', ' ', new_line)
        #new_line = re.sub(r'\}\}', ' ', new_line)

        if index%2 == 1:
            line_list = new_line.split(':')
            #print(line_list)

            pk_key = (line_list[0].split('{')[1].split('"')[1])
            pk_value = line_list[2].split("', '")[0].split('"')[1]
            print(pk_value)
            print(pk_key)
            dic[pk_key] = pk_value



        if index%2 == 0:
            line_list = new_line.split(',')
            for item in line_list:
                item_list = item.split(':')
                #print (item_list)
                if len(item_list) != 2:
                    if pivot == None:
                        pivot = item_list[0]
                        continue
                    value = dic[pivot]
                    value = value + item
                    dic[pivot] = value.replace('"','').replace(';','')
                else:
                    d_key = item_list[0].replace('{' ,'').replace('"','').replace(' ','')
                    d_value = item_list[1].replace('"','').replace('"','')
                    dic[d_key] = d_value
                    pivot = d_key
            #print(dic[' "offered"'])
            dic_list.append(dic)
            #print(dic)
            dic = {}
            pivot = None
            #print(dic_list)
        index += 1


    for item in dic_list:
        #Cor re wrangling
        try:
            co_re = item['corequisites']
            co_list = co_re.split(' ')
            # print(co_list)
            co_index = 1
            co_re = ""
            # print(len(co_list))
            if len(co_list) > 1:
                co_re = co_list[1]
                co_index += 1
                while co_index < len(co_list):
                    co_re = co_re + " " + co_list[co_index]
                    co_index += 1

            item['corequisites'] = co_re
            # print(item['corequisites'])
        except:
            print("co-re error")
            print(item)

        # enrolled wrangling
        enrolled = item['enrolled'].split(" ")[1]
        print(item)
        item['enrolled'] = enrolled


        #faculty wrangling
        try:
            faculty = item['faculty']
            facult_list = faculty.split(' ')
            # print(co_list)
            faculty_index = 1
            faculty = ""
            # print(len(co_list))
            if len(facult_list) > 1:
                faculty = facult_list[1]
                faculty_index += 1
                while faculty_index < len(facult_list):
                    faculty = faculty + " " + facult_list[faculty_index]
                    faculty_index += 1

            item['faculty'] = faculty
            # print(item['corequisites'])
        except:
            print(item)

        #locations

        locations = item['locations']
        locations_list = locations.split(' ')
        locations = ''
        for lo in locations_list:
            if lo != '':
                if locations == '':
                    if lo == 'Monash':
                        locations = lo + " " + "Online"
                    elif lo == "Online":
                        continue
                    elif lo == "South":
                        locations = lo + " " + "Africa"
                    elif lo == "Africa":
                        continue
                    else:
                        locations = lo
                else:
                    if lo == 'Monash':
                        locations = locations + " " + lo + " " + "Online"
                    elif lo == "Online":
                        continue
                    elif lo == "South":
                        locations = locations + " " + lo + " " + "Africa"
                    elif lo == "Africa":
                        continue
                    else:
                        locations = locations + " " + lo
        item['locations'] = locations

        #offered

        offered = item['offered']
        #print(offered)
        offered_list = offered.split('offerings:')
        #print(offered_list)
        if len(offered_list) != 2:
            item['offered'] = "NA"
            item['offerings'] = "NA"

        else:
            offered = offered_list[0].strip()
            item['offered'] = offered
            offerings = offered_list[1].strip()
            item['offerings'] = offerings


        #outcomes
        try:
            outcomes = item['outcomes']
            outcomes = outcomes.strip()
            item['outcomes'] = outcomes
        except:
            item['outcomes'] = 'NA'

        #points
        points = item['points']
        points = points.strip()
        item['points'] = points

        #prereq
        try:
            pre_re = item['prerequisites']
            pre_re = pre_re.strip()
            item['prerequisites'] = pre_re

        except:
            #problem.append(item['index'])
            #print(item['points'])
            points_text = item['points']
            #resetiing points
            points = points_text.split(' ')[0].strip()
            item['points'] = points
            #setting pre req
            pre_req = points_text.split(':')
            pre_req_index = 2
            prerequsite = pre_req[1]
            while pre_req_index < len(pre_req):
                prerequsite = prerequsite + " " +pre_req[pre_req_index]
                pre_req_index += 1
            item['prerequisites'] = prerequsite.strip()
            #print(item)

            #print(pre_req)


        #prohibits
        prohibits = item['prohibits']
        item['prohibits'] = prohibits.strip()

        #rating
        rating = item['rating']
        item['rating'] = rating.strip()

        #responded
        responded = item['responded']
        item['responded'] = responded.strip()

        #Similar --- to be modified later
        similar = item['similar']
        item['similar'] = similar.strip()

        #student statisfaction
        stu = item['student_satisfaction']
        item['student_satisfaction'] = stu.strip()

        #synopsis
        try:
            syn = item['synopsis']
            item['synopsis'] = syn.strip()

        except:
            stu_text = item['student_satisfaction']
            stu = stu_text.split(' ')[0].strip()
            item['student_satisfaction'] = stu
            syn = stu_text.split(':')
            syn_text = syn[1].strip()
            syn_index = 2
            while syn_index < len(syn):
                syn_text = syn_text + " " + syn[syn_index]
                syn_index += 1
            item['synopsis'] = syn_text
            #print(item)


        #teaching_periods
        teaching_period = item['teaching_periods']
        item['teaching_periods'] = teaching_period.strip()


        #unit_code
        unit_code = item['unit_code']
        item['unit_code'] = unit_code.strip()

        #unit_name
        try:
            unit_name = item['unit_name']
            item['unit_name'] = unit_name.strip()
        except:
            unit_code_text = item['unit_code']
            unit_code = unit_code_text.split(' ')[0]
            item['unit_code'] = unit_code.strip()
            unit_name_list = unit_code_text.split(':')
            unit_index = 2
            unit_name = unit_name_list[1].strip()
            while unit_index < len(unit_name_list):
                unit_name = unit_name + " " + unit_name_list[unit_index]
                unit_index += 1
            item['unit_name'] = unit_name.strip()
            #print(item)

        #unit_type
        unit_type = item['unit_type'].strip().replace('}','').replace('\n','').strip()
        item['unit_type'] = unit_type


        if item['index'] == 'FIT5133':
            item['corequisites'] = 'For all students other than those enrolled in the Master of Business: FIT9123 or FIT5123 or FIT9006 or equivalent'



new_list = []
for item in dic_list:
    key = item['index']
    new_dic = {}
    new_dic[key] = item
    new_list.append(new_dic)

with open('fit_check.json', "w") as fit:
    #for item in new_list:
    json.dump(new_list,fit)







    #print(item)
    #print(problem)

    #print(of_in)
    #print(dic_list)

    #w.write(str(dic_list))









