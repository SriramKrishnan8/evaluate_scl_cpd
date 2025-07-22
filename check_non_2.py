import sys

script, in_, cnt_, out_ = sys.argv

in_file = open(in_, 'r')
in_content = in_file.read()
in_file.close()
in_lines = in_content.split('\n')

cnt_file = open(cnt_, 'r')
cnt_content = cnt_file.read()
cnt_file.close()
cnt_lines = cnt_content.split('\n')

i = 0
c = 0

new_lines = []
overall_count = 0

while i < len(in_lines) and c < len(cnt_lines):
    split_line = in_lines[i].split('\t')
    cnt_split_line = cnt_lines[c].split('\t')
    
    cur_cnt = int(cnt_split_line[1].strip())
    print(cur_cnt)

    if cur_cnt == 1:
        i += 1
        c += 1
        print(f"Skipping {split_line[0]} {split_line[1]}")
        continue

    j = cur_cnt
    overall_count += cur_cnt
    while j > 0:
        print(f"Adding {in_lines[i]}")
        new_lines.append(f"{in_lines[i]}")
        j -= 1
        i += 1
    
    c += 1

with open(out_, 'w') as out_file:
    out_file.write('\n'.join(new_lines) + '\n')

print(f"Overall count: {overall_count}")