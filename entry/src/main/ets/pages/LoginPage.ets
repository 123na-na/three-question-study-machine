import router from '@ohos.router';
import { getNickname, setNickname, getUserId } from '../service/AuthService';
import { loadSampleCoursesIfNeeded } from '../service/SampleCourseLoader';
import { Spacing } from '../constants/Theme';
import { Colors } from '../constants/Theme';
import { Radius } from '../constants/Theme';
import { promptAction } from '@kit.ArkUI';

@Entry
@Component
struct LoginPage {
  @State nickname: string = '';
  @State isLoading: boolean = false;
  @State showSlogan: boolean = false;

  aboutToAppear(): void {
    getNickname().then((name) => {
      if (name) {
        this.nickname = name;
      }
    });
    setTimeout(() => {
      this.showSlogan = true;
    }, 300);
  }

  build() {
    Column() {
      // Logo & Title
      Column() {
        Text('📖')
          .fontSize(64)
          .margin({ bottom: Spacing.md })

        Text('三问高效学习机')
          .fontSize(28)
          .fontWeight(FontWeight.Bold)
          .fontColor(Colors.TEXT)

        Text('是什么 → 为什么 → 怎么用')
          .fontSize(15)
          .fontColor(Colors.TEXT_SECONDARY)
          .margin({ top: Spacing.sm, bottom: Spacing.xl })
          .textAlign(TextAlign.Center)
          .opacity(this.showSlogan ? 1 : 0)
          .animation({ duration: 800, curve: Curve.Linear })
      }
      .width('100%')
      .padding({ top: 60, bottom: 40 })
      .justifyContent(FlexAlign.Center)
      .alignItems(HorizontalAlign.Center)

      // Nickname Input
      Column() {
        TextInput({ placeholder: '输入昵称开始学习', text: this.nickname })
          .width('85%')
          .height(48)
          .fontSize(16)
          .placeholderColor(Colors.TEXT_LIGHT)
          .borderRadius(Radius.lg)
          .backgroundColor(Colors.CARD)
          .border({ width: 1, color: Colors.BORDER })
          .padding({ left: Spacing.lg })
          .maxLength(20)
          .onChange((val: string) => {
            this.nickname = val.trim();
          })
      }
      .width('100%')
      .alignItems(HorizontalAlign.Center)
      .margin({ bottom: Spacing.xxl })

      // Start Button
      Button('开始学习')
        .width('85%')
        .height(50)
        .backgroundColor(Colors.PRIMARY)
        .borderRadius(Radius.lg)
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
        .enabled(this.nickname.length > 0 && !this.isLoading)
        .opacity(this.nickname.length > 0 ? 1 : 0.5)
        .onClick(() => {
          this.startLearning();
        })

      // Loading indicator
      if (this.isLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: Spacing.lg })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
    .linearGradient({
      direction: GradientDirection.Bottom,
      colors: [['#EFF6FF', 0], ['#F1F5F9', 1]]
    })
    .justifyContent(FlexAlign.Start)
    .alignItems(HorizontalAlign.Center)
  }

  async startLearning(): Promise<void> {
    if (!this.nickname || this.nickname.trim().length === 0) {
      return;
    }
    this.isLoading = true;
    try {
      console.info('[LoginPage] Starting learning with nickname: ' + this.nickname);
      await setNickname(this.nickname);
      await getUserId();
          
      console.info('[LoginPage] Loading sample courses...');
      await loadSampleCoursesIfNeeded();
          
      console.info('[LoginPage] Navigation to HomePage');
      router.replaceUrl({ url: 'pages/HomePage' });
    } catch (err) {
      promptAction.showToast({ message: '初始化失败，请重试', duration: 2000 });
      console.error('[LoginPage] startLearning error: ' + JSON.stringify(err));
    } finally {
      this.isLoading = false;
    }
  }
}
