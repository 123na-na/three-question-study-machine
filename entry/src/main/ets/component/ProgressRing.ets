@Component
export struct ProgressRing {
  @Prop percent: number;
  @Prop ringSize: number;
  @Prop strokeWidth: number;
  @Prop color: string;
  @Prop bgColor: string;
  @Prop showText: boolean;

  build() {
    Stack({ alignContent: Alignment.Center }) {
      Circle()
        .width(this.ringSize)
        .height(this.ringSize)
        .fill(Color.Transparent)
        .stroke(this.bgColor)
        .strokeWidth(this.strokeWidth)

      Circle()
        .width(this.ringSize)
        .height(this.ringSize)
        .fill(Color.Transparent)
        .stroke(this.color)
        .strokeWidth(this.strokeWidth)
        .strokeDashArray(this.getDashArray())
        .rotate({ angle: -90, centerX: this.ringSize / 2, centerY: this.ringSize / 2 })

      if (this.showText) {
        Text(`${Math.round(this.percent)}%`)
          .fontSize(this.ringSize * 0.18)
          .fontColor(this.color)
          .fontWeight(FontWeight.Bold)
      }
    }
    .width(this.ringSize)
    .height(this.ringSize)
  }

  getDashArray(): number[] {
    const radius = (this.ringSize - this.strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const p = Math.max(0, Math.min(this.percent, 100)) / 100;
    return [circumference * p, circumference];
  }
}
