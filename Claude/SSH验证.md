最靠谱的办法不是“猜它是不是那台”，而是**在这台虚拟机里做可验证标记**，然后让 Claude 读出来。

你可以这样确认。

先看这台机子的唯一信息：

```bash
hostname
hostname -f
uname -n
cat /etc/hostname
ip addr
whoami
pwd
```

再拿几个更强的标识：

```bash
cat /etc/machine-id
dmidecode -s system-uuid 2>/dev/null
lsblk
df -h
```

如果 Claude 回答里读到的这些值，和你 SSH 上去看到的一致，那它操作的就是这台。

更直接一点，你可以主动放一个“只有这台机子才有”的标记文件：

```bash
echo "THIS_IS_VM_A_20260314" > /root/.vm_marker
cat /root/.vm_marker
```

然后让 Claude 执行：

```bash
cat /root/.vm_marker
```

它如果能读到同样内容，基本就坐实了。

想更稳，可以让它创建一个临时文件，再由你自己检查：

```bash
touch /tmp/claude_was_here_001
ls -l /tmp/claude_was_here_001
```

或者让 Claude 创建：

```bash
echo "created by claude" > /tmp/claude_check
```

你再 SSH 里看：

```bash
cat /tmp/claude_check
```

能对上，就说明 Claude 确实在这台虚拟机里执行了命令。

还有几个很好用的交叉验证点：

```bash
who
w
ps -ef | grep -i claude
history | tail -20
```

如果 Claude 是通过当前 SSH 会话或相关代理在跑，有时能从会话、进程、历史里看到痕迹。不过这个不如“标记文件法”稳定。

我更推荐你以后固定用这套：

1. 登录后先看 `hostname` 和 `cat /etc/machine-id`
    
2. 写一个标记文件 `/root/.vm_marker`
    
3. 让 Claude 先读标记文件再干活
    
4. 干完后让 Claude 写一个结果文件，你再本机检查
    

这样不会串机器，特别适合多台 VM 长得很像的时候。

你要的话，我可以直接给你一套“防止 Claude 连错机器”的开场检查脚本。