"""Part 8: Rewrite ProfileTab.ets with function-based API"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Restored: {rel_path}')

write_file('component/ProfileTab.ets', """\
import { router } from '@kit.ArkUI';
import { getAllCourses, getKnowledgePointsByCourse, getSessionByKpAndStep, getPreference, setPreference } from '../service/DatabaseHelper';
import { getNickname } from '../service/AuthService';
import { setBaseUrl } from '../service/AIService';
import { ScoreCalculator } from '../utils/ScoreCalculator';
import { Colors, Radius } from '../constants/Theme';

@Component
export struct ProfileTab {
  @State userName: string = '学习者';
  @State backendUrl: string = '';
  @State aboutExpanded: boolean = false;
  @State totalCourses: number = 0;
  @State completedKp: number = 0;
  @State avgScore: number = 0;
  @State isLoading: boolean = true;

  async aboutToAppear() {
    try {
      const savedUrl = await getPreference('backend_url');
      this.backendUrl = savedUrl || '';
      this.userName = (await getNickname()) || '学习者';
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
    await this.loadStats();
  }

  async loadStats() {
    try {
      const courses = await getAllCourses();
      this.totalCourses = courses.length;

      let completedCount = 0;
      let totalScore = 0;
      let scoreCount = 0;
      for (const course of courses) {
        const kps = await getKnowledgePointsByCourse(course.id);
        for (const kp of kps) {
          const what = await getSessionByKpAndStep(kp.id as number, 'what');
          const why = await getSessionByKpAndStep(kp.id as number, 'why');
          const how = await getSessionByKpAndStep(kp.id as number, 'how');
          if (what?.status === 'completed' && why?.status === 'completed' && how?.status === 'completed') {
            completedCount++;
            totalScore += ScoreCalculator.calculateOverallScore(
              what!.score as number, why!.score as number, how!.score as number
            );
            scoreCount++;
          }
        }
      }
      this.completedKp = completedCount;
      this.avgScore = scoreCount > 0 ? Math.round(totalScore / scoreCount) : 0;
      this.isLoading = false;
    } catch (error) {
      console.error('Failed to load profile stats:', error);
      this.isLoading = false;
    }
  }

  async saveBackendUrl() {
    try {
      await setPreference('backend_url', this.backendUrl);
      await setBaseUrl(this.backendUrl);
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  }

  build() {
    Column() {
      Column() {
        Text('我的')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .fontColor(Colors.PRIMARY)

        Text('个人中心')
          .fontSize(13)
          .fontColor(Colors.TEXT_SECONDARY)
          .margin({ top: 4 })
      }
      .width('100%')
      .padding({ top: 20, bottom: 16, left: 20, right: 20 })
      .alignItems(HorizontalAlign.Start)
      .backgroundColor('#EFF6FF')

      if (this.isLoading) {
        Column() {
          LoadingProgress()
            .width(36)
            .height(36)
            .color(Colors.PRIMARY)
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        Scroll() {
          Column() {
            // Profile card
            Column() {
              Stack() {
                Circle()
                  .width(72)
                  .height(72)
                  .fill('#DBEAFE')

                Text('👤')
                  .fontSize(32)
              }

              Text(this.userName)
                .fontSize(20)
                .fontWeight(FontWeight.Bold)
                .fontColor(Colors.TEXT)
                .margin({ top: 12 })

              Text('坚持学习，每天进步')
                .fontSize(13)
                .fontColor(Colors.TEXT_SECONDARY)
                .margin({ top: 4 })

              Row() {
                this.profileStat(`${this.totalCourses}`, '课程', Colors.PRIMARY)
                this.profileStat(`${this.completedKp}`, '已掌握', Colors.SUCCESS)
                this.profileStat(`${this.avgScore}`, '平均分', Colors.WARNING)
              }
              .width('100%')
              .margin({ top: 20 })
              .padding({ top: 16 })
              .border({ width: { top: 1 }, color: Colors.BORDER })
            }
            .width('100%')
            .padding(20)
            .backgroundColor(Colors.CARD)
            .borderRadius(Radius.lg)
            .shadow({ radius: 8, color: '#0000000d', offsetX: 0, offsetY: 2 })
            .margin({ left: 20, right: 20, top: 16 })
            .alignItems(HorizontalAlign.Center)

            // Settings card
            Column() {
              Row() {
                Text('⚙️')
                  .fontSize(20)
                  .margin({ right: 10 })
                Text('AI 服务设置')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(Colors.TEXT)
              }
              .width('100%')
              .alignSelf(ItemAlign.Start)

              Text('后端服务地址')
                .fontSize(13)
                .fontColor(Colors.TEXT_SECONDARY)
                .alignSelf(ItemAlign.Start)
                .margin({ top: 16 })

              TextInput({ placeholder: 'http://10.0.2.2:8000', text: this.backendUrl })
                .width('100%')
                .height(44)
                .fontSize(14)
                .backgroundColor('#F1F5F9')
                .borderRadius(8)
                .padding({ left: 12, right: 12 })
                .margin({ top: 8 })
                .onChange((value: string) => {
                  this.backendUrl = value;
                })

              Button('保存设置')
                .width('100%')
                .height(44)
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .backgroundColor(Colors.PRIMARY)
                .fontColor('#FFFFFF')
                .borderRadius(999)
                .margin({ top: 16 })
                .onClick(() => {
                  this.saveBackendUrl();
                })
            }
            .width('100%')
            .padding(18)
            .backgroundColor(Colors.CARD)
            .borderRadius(16)
            .shadow({ radius: 8, color: '#0000000d', offsetX: 0, offsetY: 2 })
            .margin({ left: 20, right: 20, top: 16 })

            // About section
            Column() {
              Row() {
                Text('ℹ️')
                  .fontSize(20)
                  .margin({ right: 10 })
                Text('关于应用')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(Colors.TEXT)

                Blank()

                Text(this.aboutExpanded ? '收起 ▲' : '展开 ▼')
                  .fontSize(13)
                  .fontColor(Colors.PRIMARY)
              }
              .width('100%')
              .onClick(() => {
                this.aboutExpanded = !this.aboutExpanded;
              })

              if (this.aboutExpanded) {
                Column() {
                  Text('三问高效学习机（问枢）是一款基于"是什么→为什么→怎么用"三问学习法的知识深度理解工具。')
                    .fontSize(13)
                    .fontColor(Colors.TEXT_SECONDARY)
                    .margin({ top: 12 })

                  Text('')
                    .fontSize(8)

                  Text('技术栈: HarmonyOS ArkTS + Python FastAPI + DeepSeek AI')
                    .fontSize(12)
                    .fontColor(Colors.TEXT_LIGHT)

                  Text('')
                    .fontSize(8)

                  Text('版本: v1.0.0')
                    .fontSize(12)
                    .fontColor(Colors.TEXT_LIGHT)
                }
              }
            }
            .width('100%')
            .padding(18)
            .backgroundColor(Colors.CARD)
            .borderRadius(16)
            .shadow({ radius: 8, color: '#0000000d', offsetX: 0, offsetY: 2 })
            .margin({ left: 20, right: 20, top: 16 })

            Button('📑 查看完整学习报告')
              .width('90%')
              .height(46)
              .fontSize(15)
              .fontWeight(FontWeight.Bold)
              .backgroundColor(Colors.PRIMARY)
              .fontColor('#FFFFFF')
              .borderRadius(Radius.full)
              .margin({ top: 20 })
              .onClick(() => {
                router.pushUrl({ url: 'pages/ProgressDashboardPage' });
              })
          }
          .width('100%')
          .padding({ bottom: 24 })
        }
        .layoutWeight(1)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }

  @Builder
  profileStat(value: string, label: string, color: string) {
    Column() {
      Text(value)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(12)
        .fontColor(Colors.TEXT_SECONDARY)
        .margin({ top: 2 })
    }
    .alignItems(HorizontalAlign.Center)
    .layoutWeight(1)
  }
}
""")

print('Part 8: ProfileTab.ets rewritten with function-based API')
print('Run part 9 to clean up and verify build')