import router from '@ohos.router';
import { isLoggedIn } from '../service/AuthService';
import { initFromPreferences } from '../service/AIService';
import { getCourseCount } from '../service/DatabaseHelper';
import { loadSampleCoursesIfNeeded } from '../service/SampleCourseLoader';

@Entry
@Component
struct Index {
  @State showLoading: boolean = true;
  @State statusText: string = '加载中...';
  @State loadingOpacity: number = 1;

  aboutToAppear(): void {
    this.checkStatus();
  }

  async checkStatus(): Promise<void> {
    await initFromPreferences();
    await this.delay(800);
    const loggedIn = await isLoggedIn();
    if (loggedIn) {
      await loadSampleCoursesIfNeeded();
      const count = await getCourseCount();
      this.statusText = count > 0 ? '进入学习...' : '准备课程...';
      await this.delay(500);
      router.replaceUrl({ url: 'pages/HomePage' });
    } else {
      this.statusText = '欢迎回来';
      this.loadingOpacity = 0;
      await this.delay(300);
      router.replaceUrl({ url: 'pages/LoginPage' });
    }
  }

  delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  build() {
    Column() {
      Text('📖')
        .fontSize(64)
        .margin({ bottom: 20 })
      Text('三问高效学习机')
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor('#1E293B')
      Text('问枢')
        .fontSize(14)
        .fontColor('#94A3B8')
        .margin({ top: 8 })
      if (this.showLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color('#3B82F6')
          .margin({ top: 40 })
        Text(this.statusText)
          .fontSize(14)
          .fontColor('#94A3B8')
          .margin({ top: 12 })
          .opacity(this.loadingOpacity)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F8FAFC')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}
