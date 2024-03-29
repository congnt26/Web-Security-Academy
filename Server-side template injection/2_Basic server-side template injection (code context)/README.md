# Basic server-side template injection (code context)
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context

## Phân tích
- Login default user (wiener)
- Dạo qua các function như 
  - View post/post comment 
    - Using Hacktricks to Fuzz Comments --> _Failed_ vì ta thử các payload nhưng nó ko valuated
    ![img_1.png](img_1.png)
    - Ta thấy tên của người dùng đc reflect trong các post.
  - Update *Preferred name*
  ![img.png](img.png)
    - Để ý thấy `blog-post-author-display` sẽ hiển thị theo user.name, user.first_name, or user.nickname
- Để detect SSTI, ngoài dùng các payload có sẵn, ta có thể dùng error message để xác định template engine đang sử dụng
- Gởi req với invalid name và refresh bài post trên browser
![img_2.png](img_2.png)
![img_3.png](img_3.png)
  - Note: ta thấy error message trên bài post vì do nó đang xài template có object là user và attribute là name, ở đây attribute bị sai nên ko hiển thị lên được --> báo error ngay trên post web UI.
- Ta xác định đc template engine đang dùng là `Tornado`, syntax là `{{someExpression}}` --> dùng các payload trong [Hacktrick](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#tornado-python) của Tornado để exploit
- Ví dụ `{% import os %}{{os.system('whoami')}}`
![img_4.png](img_4.png)
- Lỗi syntax
![img_5.png](img_5.png)
- Vì syntax của Tornado phải là `{{someExpression}}`, trong khi ở đây bắt đầu bằng `{% import os %} ...`
- Hãy tưởng tượng underlying code của UI sẽ là
![img_7.png](img_7.png)
- Nếu là chèn thêm payload để exploit thì phải thêm `}}` để close-off cái user.name object lại 
![img_6.png](img_6.png)
- Do đó input sẽ phải là `user.name }}{{ PAYLOAD to exploit }}`
![img_8.png](img_8.png)
- Kết quả là đã exploit được user
![img_9.png](img_9.png)
- Ta thấy whoami là carlos, check tiếp `pwd` và `ls` cmd
![img_10.png](img_10.png)
![img_11.png](img_11.png)

## Resolve lab
- Tiến hành xóa file morale.txt
![img_12.png](img_12.png)
- Done!!
![img_13.png](img_13.png)

## Recap
- Ta có thể detect template engine bằng 2 cách
- Trong bài này, ta dùng cách 2
![img_14.png](img_14.png)