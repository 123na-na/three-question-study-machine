import { Colors, Spacing, Radius } from '../constants/Theme';

import { getReviewsDue } from '../service/DatabaseHelper';

import router from '@ohos.router';



interface ReviewDueItem {
  id: number;
  knowledge_point_id: number;
  ease_factor: number;
  interval_days: number;
  next_review_date: string;
  review_count: number;
  avg_score: number;
  kp_title: string;
  course_name: string;
}

@Component

export struct ReviewTab {

  @State reviewsDue: ReviewDueItem[] = [];

  @State isLoading: boolean = true;



  aboutToAppear(): void {

    this.loadReviews();

  }



  async loadReviews(): Promise<void> {

    try {

      this.reviewsDue = await getReviewsDue();

      this.isLoading = false;

    } catch (err) {

      console.error('[ReviewTab] loadReviews error: ' + JSON.stringify(err));

      this.isLoading = false;

    }

  }



  build() {

    Column() {

      Text('待复习')

        .fontSize(18)

        .fontWeight(FontWeight.Medium)

        .fontColor(Colors.TEXT)

        .width('100%')

        .margin({ bottom: Spacing.md })



      if (this.isLoading) {

        LoadingProgress()

          .width(24)

          .height(24)

          .color(Colors.PRIMARY)

          .margin({ top: 20 })

      } else if (this.reviewsDue.length === 0) {

        Column() {

          Text('✅')

            .fontSize(32)

          Text('当前没有待复习内容')

            .fontSize(14)

            .fontColor(Colors.TEXT_SECONDARY)

            .margin({ top: Spacing.sm })

        }

        .width('100%')

        .alignItems(HorizontalAlign.Center)

        .padding({ top: 30, bottom: 30 })

      } else {

        List() {

          ForEach(this.reviewsDue, (item: ReviewDueItem) => {

            ListItem() {

              ReviewCard({ item: item })

            }

          }, (item: ReviewDueItem) => item.id.toString())

        }

        .width('100%')

        .layoutWeight(1)

      }

    }

    .width('100%')

    .padding(Spacing.lg)

  }

}



@Component

struct ReviewCard {

  item: ReviewDueItem = { id: 0, knowledge_point_id: 0, ease_factor: 0, interval_days: 0, next_review_date: '', review_count: 0, avg_score: 0, kp_title: '', course_name: '' };



  build() {

    Column() {

      Row() {

        Text('🔄')

          .fontSize(24)

        Column() {

          Text(this.item.course_name + ' - ' + this.item.kp_title)

            .fontSize(14)

            .fontWeight(FontWeight.Medium)

            .fontColor(Colors.TEXT)

            .maxLines(1)

            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text('上次评分: ' + Math.round(this.item.avg_score) + '分')

            .fontSize(12)

            .fontColor(Colors.TEXT_SECONDARY)

            .margin({ top: 2 })

        }

        .layoutWeight(1)

        .margin({ left: Spacing.md })

        Text('复习')

          .fontSize(13)

          .fontColor(Colors.PRIMARY)

          .fontWeight(FontWeight.Medium)

      }

      .width('100%')

    }

    .padding(Spacing.md)

    .backgroundColor(Colors.CARD)

    .borderRadius(Radius.sm)

    .shadow({ radius: 2, color: Colors.SHADOW })

    .margin({ bottom: Spacing.sm })

    .onClick(() => {
      router.pushUrl({
        url: 'pages/ReviewSessionPage',
        params: { kpId: this.item.knowledge_point_id }
      });

    })

  }

}

