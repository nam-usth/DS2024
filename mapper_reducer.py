from pyspark import SparkContext

# Hàm Mapper: Chuyển từng dòng đầu vào thành cặp (depth, path)
def mapper(line):
    path = line.strip()  # Loại bỏ khoảng trắng
    depth = path.count('/')  # Đếm số lượng dấu '/'
    return (depth, path)

# Hàm Reducer: Nhóm các đường dẫn theo độ sâu và tìm đường dẫn dài nhất
def reducer(a, b):
    # Giữ lại đường dẫn dài nhất trong nhóm
    if len(a) >= len(b):
        return a
    else:
        return b

# Khởi tạo SparkContext
sc = SparkContext('local', 'Longest Path by Depth')

# Đọc dữ liệu đầu vào từ thư mục input_data/
input_data = sc.textFile("input_data/*")

# Áp dụng hàm Mapper để tạo cặp (depth, path)
mapped_data = input_data.map(mapper)

# Thực hiện Reduce để tìm đường dẫn có độ sâu lớn nhất và là đường dẫn dài nhất
# Trong mỗi nhóm (theo độ sâu), chỉ giữ lại đường dẫn dài nhất
reduced_data = mapped_data.reduceByKey(reducer)

# Tìm đường dẫn có độ sâu (depth) lớn nhất
longest_path = reduced_data.max(lambda x: x[0])  # Tìm depth lớn nhất và đường dẫn tương ứng

# In kết quả ra màn hình (để kiểm tra)
print("Longest Path: ", longest_path)

# Xóa thư mục output nếu đã tồn tại
import shutil
import os
output_dir = "final_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# Ghi kết quả vào tệp
os.makedirs(output_dir, exist_ok=True)
with open(f"{output_dir}/longest_path.txt", "w") as output_file:
    output_file.write(f"Longest Path: {longest_path[1]}\nNumber of '/' characters: {longest_path[0]}")

print(f"Final output has been saved to {output_dir}/longest_path.txt")
