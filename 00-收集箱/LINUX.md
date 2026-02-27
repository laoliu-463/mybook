`bin boot cdrom dev etc home lib lib32 lib64 libx32 lost+found media mnt opt proc root run sbin snap srv sys tmp usr var swapfile`

### 新手必须优先记住的 10 个（够你用到工作）

- **`/home`**：所有普通用户的家目录（你的就是 `/home/caojianing`）
    
- **`/etc`**：系统/服务的配置文件（比如 nginx、ssh 配置都在这附近）
    
- **`/var`**：经常变化的数据（**日志**、缓存、数据库数据等）
    
    - 日志常在：`/var/log`
        
- **`/usr`**：系统安装的大部分程序和库（很多软件会在这里）
    
- **`/tmp`**：临时文件（重启可能清）
    
- **`/bin`**：常用基本命令（ls、cp、mv 等）
    
- **`/sbin`**：系统管理命令（偏管理员用）
    
- **`/root`**：root 管理员的家目录（别乱动）
    
- **`/dev`**：设备文件（硬盘、网卡、终端都在这“映射”）
    
- **`/proc`**：进程/内核信息（虚拟文件系统，别当成真实文件夹）
    

### 你列表里几个“看着陌生但正常”的

- **`lost+found`**：磁盘文件系统修复时用（正常存在）
    
- **`media`**：自动挂载 U 盘/移动硬盘的位置
    
- **`mnt`**：手动挂载用（你自己挂载磁盘/共享目录会用到）
    
- **`snap`**：Snap 包管理相关
    
- **`swapfile`**：交换空间文件（相当于“虚拟内存”）

