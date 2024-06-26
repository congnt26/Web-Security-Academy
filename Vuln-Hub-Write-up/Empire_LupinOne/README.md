# *Empire: LupinOne* - Vuln Hub lab practice
- VM URL: https://www.vulnhub.com/entry/empire-lupinone,750/
- Download và giải nén, import vào VMWare để tạo máy ảo
![img.png](img.png)
- Note: IP sẽ được tạo tự động, ở đây là `192.168.67.131`

## Tiến hành recon và exploit:

- Scan nmap để tìm hết các port đang mở
![img_1.png](img_1.png)
- Ta thấy có port 22, 80, tiếp tục scan 2 ports này
![img_2.png](img_2.png)
- Access web port 80 --> nothing
![img_3.png](img_3.png)
- Ta thấy có file robots.txt với `Disallow: /~myfiles`  --> Error 404
![img_4.png](img_4.png)
- Dùng kĩ thuật fuzz để tìm các hidden folder --> ko thấy gì đặc biệt
![img_5.png](img_5.png)
- Để ý dấu `~` trong myfiles, ta fuzz với ~ prefix này
![img_6.png](img_6.png)
- Thấy có `secret` file
![img_7.png](img_7.png)
- Tiếp tục tìm kiếm private key với fuzz, note là ssh username = icex64, dùng ffuf thì ko thấy file nào xuất hiện.
- Do đó phải thay đổi cách tìm kiếm như trên (dùng ~), nhưng ở đây là file ẩn (hidden), mà trong linux, các file này thường sẽ có dấu `.` ở đầu file.
![img_8.png](img_8.png)
- Kết quả có file `.mysecret.txt`
![img_9.png](img_9.png)
![img_10.png](img_10.png)
- Nó được encode bởi Base`xx`, dùng https://www.dcode.fr/cipher-identifier để analyse
![img_11.png](img_11.png)
- Chuỗi này dùng Base58 để encode, ta dùng [CyberChef](https://gchq.github.io/CyberChef) để decode
![img_12.png](img_12.png)
- Great, nó là 1 file private ssh key, tải file này về với tên id_rsa
![img_13.png](img_13.png)
- Ah, ta cần 1 passphrase nữa. Trong pentest, ta thường dùng John the Ripper để crack password.
- Dùng ssh2john để convert private sang hash
![img_14.png](img_14.png)
- Dùng John để crack với fasttrack wordlist
![img_15.png](img_15.png)
- Check again, pass là `P@55w0rd!`
![img_16.png](img_16.png)
- Login thành công
![img_17.png](img_17.png)
- Cat user.txt
![img_18.png](img_18.png)

## Privilege Escalation
- Check `sudo -l` --> đây luôn là command check trước tiên khi login vào máy linux, vì nó chứa các thông tin của user hoặc root, file permission. 
![img_19.png](img_19.png)
- Ta thấy user icex64 có thể run file heist.py as arsene user và nó nằm trong /home/arsene folder.
![img_20.png](img_20.png)
- Check nội dung thì thấy nó import 1 webbrowser library
- Locate và check permission lib này --> writeable bởi everyone --> tận dụng file này để conduct privilege escalation.
![img_21.png](img_21.png)
- Ta edit file với nano và include a Python reverse shell code (https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#python) trong hàm open()
![img_22.png](img_22.png)

    ![img_23.png](img_23.png)
- Mở nc trên máy kali (attacker) để listen on port 9988 sau đó Run file trên target -> reverse shell is running.
![img_24.png](img_24.png)
- Do reverse shell nên nó (target: 67.131) sẽ tự connect back về attacker (Kali: 67.135), do đó trên máy kali , ta sẽ thấy
![img_25.png](img_25.png)
- Check 1 số file thì thấy có file .secret chứa password của arsene user.
![img_26.png](img_26.png)
- Ở đây có 2 cách để tiếp tục exploit:
  - Cách 1: dùng password này để su từ icex64 qua arsene user.
  ![img_27.png](img_27.png)
  - Check sudo -l
  ![img_28.png](img_28.png)
  - User arsene có thể run pip as root without needing a password, vào GTFObins (https://gtfobins.github.io/gtfobins/pip/#sudo) ta thấy rằng pip used as sudo có thể privilege escalation
  
  `````
    TF=$(mktemp -d)
    echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > $TF/setup.py
    sudo pip install $TF
  `````
  - Và có thể escalate lên root :)
  ![img_29.png](img_29.png)
  - Từ đó có thể get file root.txt, đây là mục đích cuối cùng của bài này
  ![img_30.png](img_30.png)
  ![img_31.png](img_31.png)

- Cách 2: upgrade shell
  - Ở nc listening trên máy kali, dùng kĩ thuật upgrade shell trực tiếp trên terminal, ko cần phải su user như cách 1.
  ![img_32.png](img_32.png)
  - Lặp lại sudo -l và lợi dụng lỗ hổng của pip để run với root user.

### Cuối cùng đã done với Empire-Lupin One lab.