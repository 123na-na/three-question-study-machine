import { getCourseCount, addCourse, addKnowledgePoint } from './DatabaseHelper';

interface SampleKP {
  title: string;
  content: string;
}

interface SampleCourse {
  name: string;
  description: string;
  knowledgePoints: SampleKP[];
}

const SAMPLE_COURSES: SampleCourse[] = [
  {
    name: 'Python 编程入门',
    description: '学习 Python 编程语言的基础知识，包括变量、数据类型、控制流和函数',
    knowledgePoints: [
      { title: '变量与数据类型', content: 'Python 中的变量不需要声明类型，可以直接赋值。常见数据类型包括整数(int)、浮点数(float)、字符串(str)、布尔值(bool)、列表(list)、元组(tuple)、字典(dict)等。' },
      { title: '条件语句与循环', content: '条件语句使用 if/elif/else 进行分支判断。循环包括 for 循环（用于遍历可迭代对象）和 while 循环（条件满足时持续执行）。' },
      { title: '函数定义与使用', content: '函数使用 def 关键字定义。支持位置参数、默认参数、关键字参数和可变参数。函数可以返回值，也可以返回多个值（实际是元组）。' },
    ]
  },
  {
    name: '数据结构与算法',
    description: '掌握常用的数据结构和经典算法，提升编程解决问题的能力',
    knowledgePoints: [
      { title: '数组与链表', content: '数组是连续内存空间上相同类型元素的集合，支持随机访问。链表由节点组成，每个节点包含数据和指向下一个节点的指针，分为单链表、双链表和循环链表。' },
      { title: '栈与队列', content: '栈是后进先出(LIFO)的数据结构，主要操作有入栈(push)和出栈(pop)。队列是先进先出(FIFO)的数据结构，主要操作有入队(enqueue)和出队(dequeue)。' },
      { title: '二叉树与遍历', content: '二叉树每个节点最多有两个子节点。遍历方式包括前序遍历(根左右)、中序遍历(左根右)、后序遍历(左右根)和层序遍历。' },
    ]
  },
  {
    name: '操作系统原理',
    description: '理解操作系统核心概念：进程管理、内存管理、文件系统和设备管理',
    knowledgePoints: [
      { title: '进程与线程', content: '进程是资源分配的基本单位，线程是CPU调度的基本单位。进程间通信方式包括管道、消息队列、共享内存、信号量和套接字。多线程编程需要注意同步与互斥问题。' },
      { title: '内存管理', content: '内存管理包括内存分配与回收、地址转换、内存保护和内存扩充。虚拟内存技术允许程序执行时只将部分内容装入内存，通过页面置换算法管理。' },
      { title: '文件系统', content: '文件系统负责管理磁盘上的数据存储和检索。常见的文件系统有FAT32、NTFS、ext4等。文件系统采用目录树结构组织文件，支持文件的创建、读写、删除等操作。' },
    ]
  },
  {
    name: '计算机网络',
    description: '学习计算机网络的基本概念、协议体系结构和网络应用',
    knowledgePoints: [
      { title: 'TCP/IP 协议栈', content: 'TCP/IP 协议栈分为应用层、传输层、网络层和网络接口层。应用层协议包括HTTP、FTP、SMTP等，传输层有TCP（可靠）和UDP（快速），网络层核心是IP协议。' },
      { title: 'HTTP 协议', content: 'HTTP是超文本传输协议，基于请求-响应模型。主要方法有GET（获取资源）、POST（提交数据）、PUT（更新资源）和DELETE（删除资源）。状态码分为1xx信息、2xx成功、3xx重定向、4xx客户端错误、5xx服务器错误。' },
      { title: '网络安全基础', content: '网络安全包括机密性、完整性和可用性三大目标。常见安全技术有对称加密（AES）、非对称加密（RSA）、数字签名、数字证书、SSL/TLS协议和防火墙。' },
    ]
  },
  {
    name: '数据库系统概论',
    description: '掌握关系数据库的核心概念，SQL语言和数据库设计方法',
    knowledgePoints: [
      { title: '关系模型与SQL', content: '关系模型使用二维表表示数据，每行是一条记录，每列是一个属性。SQL包括数据定义语言(DDL)、数据操纵语言(DML)和数据控制语言(DCL)。基本操作有SELECT、INSERT、UPDATE、DELETE。' },
      { title: '数据库设计', content: '数据库设计遵循规范化理论：第一范式(1NF)要求属性不可分，第二范式(2NF)消除部分依赖，第三范式(3NF)消除传递依赖。通过ER图进行概念设计，转换为关系模型。' },
      { title: '事务与并发控制', content: '事务具有ACID特性：原子性、一致性、隔离性和持久性。并发控制主要解决丢失修改、读脏数据和不可重复读问题。封锁协议包括共享锁和排他锁，隔离级别从低到高包括READ UNCOMMITTED到SERIALIZABLE。' },
    ]
  },
];

export async function loadSampleCoursesIfNeeded(): Promise<void> {
  try {
    console.info('[SampleCourseLoader] Checking if sample courses need to be loaded...');
    const count = await getCourseCount();
    console.info('[SampleCourseLoader] Current course count: ' + count);
    
    if (count > 0) {
      console.info('[SampleCourseLoader] Sample courses already exist, skipping load');
      return;
    }
    
    console.info('[SampleCourseLoader] Loading ' + SAMPLE_COURSES.length + ' sample courses...');
    for (const course of SAMPLE_COURSES) {
      console.info('[SampleCourseLoader] Loading course: ' + course.name);
      const courseId = await addCourse(course.name, course.description, true);
      console.info('[SampleCourseLoader] Course created with id: ' + courseId);
      
      for (const kp of course.knowledgePoints) {
        console.info('[SampleCourseLoader] Adding KP: ' + kp.title);
        const kpId = await addKnowledgePoint(courseId, kp.title, kp.content);
        console.info('[SampleCourseLoader] KP created with id: ' + kpId);
      }
    }
    console.info('[SampleCourseLoader] Sample courses loaded successfully');
  } catch (err) {
    console.error('[SampleCourseLoader] Failed to load sample courses: ' + JSON.stringify(err));
  }
}
