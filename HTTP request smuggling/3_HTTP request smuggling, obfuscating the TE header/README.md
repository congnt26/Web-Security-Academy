# Lab: HTTP request smuggling, obfuscating the TE header
https://portswigger.net/web-security/request-smuggling/lab-obfuscating-te-header

## Phân tích

![img.png](img.png)

- Xác định FE
  - Reject --> FE dùng TE.
  - Ta thấy X là invalid value, expect phải là 1 hex cho chunk size
![img_3.png](img_3.png)

![img_2.png](img_2.png)

- Xác định BE
  - Accept: BE dùng TE
  - Ta thấy X bị drop tại FE do FE dùng TE. Request gởi đến BE là valid nên request gởi thành công --> 200 OK
![img_4.png](img_4.png)

![img_5.png](img_5.png)

## Phát hiện TE header obfuscation

![img_6.png](img_6.png)

- Trick : add thêm invalid TE header để BE dùng CL với điều kiện response timeout --> quay về bài TE-CL
```
Transfer-Encoding: xchunked

Transfer-Encoding : chunked

Transfer-Encoding: chunked
Transfer-Encoding: x

Transfer-Encoding:[tab]chunked

[space]Transfer-Encoding: chunked

X: X[\n]Transfer-Encoding: chunked

Transfer-Encoding
: chunked
```
![img_7.png](img_7.png)

## Xác nhận lại TE header obfuscation
![img_8.png](img_8.png)

![img_9.png](img_9.png)

![img_10.png](img_10.png)

## Resolve lab

![img_12.png](img_12.png)

![img_13.png](img_13.png)

![img_11.png](img_11.png)