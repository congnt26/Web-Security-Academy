# *Empire: Breakout* - Vuln Hub lab practice
- VM URL: https://www.vulnhub.com/entry/empire-breakout,751/
- Download và giải nén, import ova file vào VirtualBox để tạo máy ảo
![img.png](img.png)
- Note: IP sẽ được tạo tự động, ở đây là `192.168.67.130`
- Dùng nmap scan (-A)
![img_1.png](img_1.png)
- Ta thấy có các lưu ý:
  - Port 80/http default page cho Apache2 Debian
  - Port 139, 445 for samba on linux (có thể dùng enum4linux tool để scan SMB)
  - Port 10000, 20000 cho web admin
- Đầu tiên, ta access port 80 xem
![img_2.png](img_2.png)
- Dùng fuff để tìm hidden folder `ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.67.130/FUZZ -mc 200,301 -t 200`
![img_3.png](img_3.png)
- Có /manual với 301 response, check thử thì nó redirect tới Apache doc, cũng ko có gì đặc biệt
![img_4.png](img_4.png)
- Quay lại trang chính (port 80), check source code ta thấy 1 đoạn note đã đc mã hóa `++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>++++++++++++++++.++++.>>+++++++++++++++++.----.<++++++++++.-----------.>-----------.++++.<<+.>-.--------.++++++++++++++++++++.<------------.>>---------.<<++++++.++++++.`
![img_5.png](img_5.png)
- Dùng https://www.dcode.fr/cipher-identifier để check xem nó đc encrypt bởi programmation language nào.
![img_6.png](img_6.png)
- Đó chính là `BrainFuck`, hãy giải mã nó, pass là `.2uqPEfj3D<P'a-3`
![img_7.png](img_7.png)
- Cần phải tìm 1 user để login, vì có SMB port, dùng enum4linux để check xem có gì interesting.
![img_9.png](img_9.png)
![img_8.png](img_8.png)
- Ta thấy user là `cyber`
- Thử login vào webadmin ở port 10000, và 20000, thì thấy chỉ webadmin ở port 20000 là login đc với user/pass ở trên
![img_10.png](img_10.png)
- Trong admin panel, có 1 menu là Command Shell, gõ 1 số lệnh, chú ý sudo -l fail.
![img_12.png](img_12.png)
- Ta tạo 1 reverse shell để máy attacker (Kali) có thể run command trên máy victim
![img_11.png](img_11.png)
- Ở máy Kali, dùng nc cmd để listen
![img_13.png](img_13.png)
- Lưu ý dùng kĩ thuật upgrade shell để full control, kĩ thuật này có mention trong `CompTIA PenTest_ Certification All-in-One Exam Guide, Second Edition (Exam PT0-002)` doc trang 534.
![img_14.png](img_14.png)
- Note: `Using these commands, a penetration tester can transform a basic reverse shell into a more usable and robust interface, facilitating more efficient interaction with the compromised system.`
```
export TERM=xterm
python3 -c "import pty;pty.spawn('/bin/bash')"
(press CTRL+Z)
stty raw -echo;fg;reset

Explain:
1. Set Terminal Type: Ensures compatibility with terminal features.
2. Upgrade to a TTY Shell: Makes the shell interactive using Python.
3. Suspend the Shell: Temporarily pauses the shell to adjust settings.
4. Configure Terminal: Adjusts terminal settings for better interaction and brings the shell back.
5. Reset Terminal: Clears any display issues and sets up a clean environment.
```
![img_15.png](img_15.png)
- Ta ko đọc đc file .old_pass.bak vì ko có permission 
![img_16.png](img_16.png)
- Để ý ở home có file tar, getcap file này - `CAP_DAC_READ_SEARCH` - It means that it can read all the files on the system irrespective of their permissions. 
![img_17.png](img_17.png)
- Dùng tar này để tạo và giải nén file (lưu ý: khi giải nén file rar, sẽ giải nén ra `var/backup`, trong khi `/var/backup` là folder chưa file bak mà ta ko có quyền đọc)
![img_18.png](img_18.png)
- Lấy dc pass root, su root thôi
![img_19.png](img_19.png)
- Done vì đã escalate lên root user thành công.