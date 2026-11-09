@Component
export struct OnboardingOverlay {
  @State currentStep: number = 0;
  onComplete: () => void = () => {};

  steps: string[] = [
    '📖 欢迎使用三问高效学习机',
    '是什么 - 理解概念的本质',
    '为什么 - 探究原理与逻辑',
    '怎么用 - 掌握实践与应用',
  ];

  descriptions: string[] = [
    '三步学习法，系统化掌握每一个知识点',
    '首先明确学习对象的基本定义和概念',
    '深入理解背后的原理和逻辑关系',
    '最后通过实践巩固所学知识',
  ];

  build() {
    Column() {
      // Dots
      Row() {
        ForEach(this.steps, (_: string, index: number) => {
          Circle()
            .width(index === this.currentStep ? 10 : 6)
            .height(index === this.currentStep ? 10 : 6)
            .fill(index === this.currentStep ? '#3B82F6' : '#CBD5E1')
            .margin({ left: 4, right: 4 })
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .margin({ top: 40 })

      // Content
      Column() {
        Text(this.steps[this.currentStep])
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#1E293B')
          .textAlign(TextAlign.Center)
          .margin({ top: 30, bottom: 16 })
        Text(this.descriptions[this.currentStep])
          .fontSize(15)
          .fontColor('#64748B')
          .textAlign(TextAlign.Center)
          .lineHeight(22)
          .padding({ left: 30, right: 30 })
      }
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)

      // Button
      Button(this.currentStep < this.steps.length - 1 ? '下一步' : '开始学习')
        .width('80%')
        .height(50)
        .backgroundColor('#3B82F6')
        .borderRadius(12)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .margin({ bottom: 40 })
        .onClick(() => {
          if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
          } else {
            this.onComplete();
          }
        })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .borderRadius(20)
    .justifyContent(FlexAlign.SpaceBetween)
  }
}
