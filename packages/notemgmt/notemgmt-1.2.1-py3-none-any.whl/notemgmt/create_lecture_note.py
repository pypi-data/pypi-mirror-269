import argparse
import os
import shutil
import re
import datetime

def lecstr2num(x):
    doti = x.index('.')
    dashi1 = x.index('_') + 1
    dashi2 = x.index('l') - 1
    part = int(x[doti-1])
    lec_num = int(x[dashi1:dashi2])
    return (lec_num, part)
    
def main():

    home_dir = os.path.expanduser('~')
    vim_templates_path = os.path.join(home_dir,".vim/templates")
    master_skeleton_path = os.path.join(vim_templates_path, "master_skeleton.tex")
    lec_skeleton_path = os.path.join(vim_templates_path, "lecture_skeleton.tex")

    parser = argparse.ArgumentParser(description="create note")
    parser.add_argument("--lecture_title", type=str, required=False, default="Lecture Title")
    parser.add_argument("--master_name", type=str, default="master", required=False)
    args = parser.parse_args()
    mname = args.master_name
    r = r'lec\w*\.tex$'
    lec_date = datetime.date.today()
    lec_title = args.lecture_title
    lec_date_str = lec_date.strftime("%B %d, %Y")
    all_lec_files = list(filter(lambda f: re.search(r,f), os.listdir(os.getcwd())))
    #print(all_lec_files)
    all_lec_nums = [lecstr2num(x) for x in all_lec_files]
    all_lec_nums.sort()
    #print('all lec files', all_lec_files)
    if len(all_lec_nums) > 0:
        llec = all_lec_nums[-1]
        week = llec[0]
        lec = llec[1]
        print('week', week, lec)
        if lec == 2:
            lec = 1
            week += 1
        else:
            lec +=1
    else:
        week = 1
        lec = 1

    filename = f"week_{week}_lec_{lec}"
    master_fn = os.path.join(os.getcwd(), f"{mname}.tex")
    lec_fn = os.path.join(os.getcwd(), f"{filename}.tex")
    
    if not(os.path.exists(master_fn)):
        cname = input("Enter course name to create master file: ")
        shutil.copyfile(master_skeleton_path, master_fn)
        with open(master_fn, "r", encoding="utf-8") as fp:
            data = fp.readlines()
        cline = data[3]
        cline = cline.replace("Course Name", cname)
        data[3] = cline
        with open(master_fn, "w", encoding="utf-8") as fp:
            fp.writelines(data)

    shutil.copyfile(lec_skeleton_path, lec_fn)

    with open(master_fn, "r", encoding = 'utf-8') as fp:
        data = fp.readlines()
    with open(master_fn, "w", encoding = "utf-8") as fp:
        blocksi = data.index('% start lecture files block\n')
        nl = data[blocksi+1]
        nnl = data[blocksi+2]
        #print(nl)
        #print(nnl)
        sbcmd = "\subfile{\detokenize{"
        ebcmd = "}}"
        fcmd = f'{sbcmd}{lec_fn}{ebcmd}\n'
        if nl == '% end lecture files block\n':
            data.insert(blocksi+1, fcmd)
        elif nnl == '% end lecture files block\n':
            data.insert(blocksi+2, '\\newpage\n')
            data.insert(blocksi+3, fcmd)
        elif nnl == '\\newpage\n':
            data[blocksi + 1] = data[blocksi+3]
            data[blocksi + 3] = fcmd
        fp.writelines(data)

    with open(lec_fn, "r", encoding="utf-8") as fp:
        data = fp.readlines()
    tline = data[1]
    dline = data[8]
    tline = tline.replace("Lecture Title", lec_title)
    dline = dline.replace("\\today", lec_date_str)
    data[1] = tline
    data[8] = dline
    with open(lec_fn, "w", encoding="utf-8") as fp:
        fp.writelines(data)
           
