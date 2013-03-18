import json
import datetime
import time
import sys
import os
import re

"""
As well as parsing dates into cyclical forms, this also does a little basic 
string substitution to remove some disallowed characters (\t,\n) from user-supplied metadata.
"""
def DateParser():
    f = open("../metadata/field_descriptions.json", "r")
    fields = json.loads(f.read())
    f.close()
    
    fields_to_derive = []
    
    derivedFile = open("../metadata/field_descriptions_derived.json",'w')
    
    output = []
    
    for field in fields:
        if field["datatype"] == "time":
             if "derived" in field: fields_to_derive.append(field)
             else: output.append(field)
        else: output.append(field)
    
    for field in fields_to_derive:
        for derive in field["derived"]:
            if "aggregate" in derive:
                output.append({"field":'_'.join([field["field"], derive["resolution"], derive["aggregate"]]), "datatype":"time", "type":"integer", "unique":True})
            else:
                output.append({"field":'_'.join([field["field"], derive["resolution"]]), "datatype":"time", "type":"integer", "unique":True})
    
    derivedFile.write(json.dumps(output))
    derivedFile.close()
    
    order = ["year", "month", "week", "day"]
    
    f = open("../metadata/jsoncatalog_derived.txt", "w")
    
    for data in open("../metadata/jsoncatalog.txt", "r"):
        line = json.loads(data)
        for field in fields_to_derive:
            try:
                content = line[field["field"]].split('-')
                intent  = [int(item) for item in content]
            except KeyError:
                continue
            except ValueError:
                #thrown if fields are empty on taking the int
                continue
            except AttributeError:
                #Happens if it's an integer,which is a forgiveable way to enter a year:
                content = [str(line[field['field']])]
                intent = [line[field['field']]]
    
            if len(content) == 0:
                continue
            else:
                to_derive = field["derived"]
                for derive in to_derive:
                    try:
                        if "aggregate" in derive:
                            if derive["resolution"] == 'day' and derive["aggregate"] == "year":
                                line[field["field"] + "_day_year"] = str(datetime.datetime(intent[0],intent[1],intent[2]).timetuple().tm_yday)
                            if derive["resolution"] == 'month' and derive["aggregate"] == "year":
                                line[field["field"] + "_month_year"] = content[1]
                            elif derive["resolution"] == 'day' and derive["aggregate"] == "month":
                                line[field["field"] + "_day_month"] = content[2]
                            elif derive["resolution"] == 'week' and derive["aggregate"] == "year":
                                yearday = datetime.datetime(intent[0],intent[1],intent[2]).timetuple().tm_yday
                                line[field["field"] + "_week_year"] = str(int(yearday/7))
                            else: continue
                        else:
                            if derive["resolution"] == 'year':
                                line[field["field"] + "_year"] = content[0]
                            elif derive["resolution"] == 'month':
                                line[field["field"] + "_month"] = str(int((datetime.date(intent[0],intent[1],1) - datetime.date(1,1,1)).days))
                            elif derive['resolution'] == 'week':
                                line[field['field'] + "_week"] = str(int((datetime.date(intent[0],intent[1],intent[2]) - datetime.date(1,1,1)).days/7)*7)
                            elif derive["resolution"] == 'day':
                                line[field["field"] + "_day"] = str((datetime.datetime.strptime('%02d'%int(content[2])+'%02d'%int(content[1])+content[0], "%d%m%Y").date() - datetime.date(1,1,1)).days)
                            else: continue
                    except ValueError:
                        #one of out a million Times articles threw this with a year of like 111,203.
                        #It's not clear how best to handle this.
                        print "Something's wrong with " + line[field["field"]] + " as a date--moving on..."
                        pass
                line.pop(field["field"])
        dumped = json.dumps(line)
        #absolutely no tabs or newlines are allowed in the json: this takes them out.
        #This doesn't do precisely the right thing if they're trying to write a literal sequence with multiple escapes.
        dumped = re.sub(r"\\[tn]",r"",dumped);
        f.write(dumped + '\n')
    
    f.close()
