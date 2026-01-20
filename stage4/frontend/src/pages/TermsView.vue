<template>
  <div class="terms-page">
    <v-container class="py-16 text-center">
      <v-chip color="primary" variant="tonal" class="mb-4 font-weight-bold px-6"
        >اتفاقية الاستخدام</v-chip
      >
      <h1 class="text-h2 font-weight-black mb-4 vibrant-gradient-text">الشروط والأحكام</h1>
      <p class="text-subtitle-1 text-grey-darken-1 font-weight-medium">
        بباستخدامك لمنصة أتراب، فإنك توافق على الالتزام بالشروط التالية
      </p>
    </v-container>

    <v-container class="pb-16">
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="glass-card pa-8 pa-md-12">
            <section class="mb-10 text-right">
              <h2 class="text-h4 font-weight-bold mb-6 text-primary">1. قبول الشروط</h2>
              <p class="text-body-1 text-grey-darken-2 lh-relaxed">
                من خلال الوصول إلى منصة أتراب واستخدامها، فإنك تقر بأنك قرأت وفهمت ووافقت على
                الالتزام بهذه الشروط والأحكام. إذا كنت لا توافق على أي جزء من هذه الشروط، فيرجى عدم
                استخدام المنصة.
              </p>
            </section>

            <v-divider class="mb-10 opacity-10"></v-divider>

            <section class="mb-10 text-right">
              <h2 class="text-h4 font-weight-bold mb-6 text-primary">2. سلوك المستخدم</h2>
              <p class="text-body-1 text-grey-darken-2 lh-relaxed mb-4">
                بصفتك مستخدماً للمنصة، فإنك تتعهد بـ:
              </p>
              <ul class="standard-list text-grey-darken-2">
                <li>استخدام المنصة للأغراض التعليمية والأكاديمية فقط.</li>
                <li>عدم نشر أي محتوى مسيء، غير قانوني، أو ينتهك حقوق الآخرين.</li>
                <li>احترام حقوق الملكية الفكرية للمواد والمصادر التعليمية المشاركة.</li>
                <li>
                  عدم محاولة الوصول غير المصرح به إلى أنظمة المنصة أو حسابات المستخدمين الآخرين.
                </li>
              </ul>
            </section>

            <v-divider class="mb-10 opacity-10"></v-divider>

            <section class="mb-10 text-right">
              <h2 class="text-h4 font-weight-bold mb-6 text-primary">3. الحساب والأمان</h2>
              <p class="text-body-1 text-grey-darken-2 lh-relaxed">
                أنت مسؤول عن الحفاظ على سرية معلومات حسابك وكلمة المرور الخاصة بك. كما تتحمل
                المسؤولية الكاملة عن جميع الأنشطة التي تحدث تحت حسابك. يجب عليك إخطارنا فوراً بأي
                استخدام غير مصرح به لحسابك.
              </p>
            </section>

            <v-divider class="mb-10 opacity-10"></v-divider>

            <section class="mb-10 text-right">
              <h2 class="text-h4 font-weight-bold mb-6 text-primary">4. الملكية الفكرية</h2>
              <p class="text-body-1 text-grey-darken-2 lh-relaxed">
                جميع المحتويات والعلامات التجارية والبرمجيات الخاصة بمنصة أتراب هي ملكية خاصة لنا
                ومحمية بموجب قوانين الملكية الفكرية. يُمنع منعاً باتاً نسخ أو تعديل أو توزيع أي جزء
                من المنصة دون إذن خطي مسبق.
              </p>
            </section>

            <v-divider class="mb-10 opacity-10"></v-divider>

            <section class="text-right">
              <h2 class="text-h4 font-weight-bold mb-6 text-primary">5. تحديد المسؤولية</h2>
              <p class="text-body-1 text-grey-darken-2 lh-relaxed">
                يتم تقديم المنصة "كما هي" دون أي ضمانات من أي نوع. نحن لا نتحمل المسؤولية عن أي
                أضرار مباشرة أو غير مباشرة ناتجة عن استخدامك للمنصة أو عدم قدرتك على استخدامها، بما
                في ذلك الأخطاء في المحتوى التعليمي المشارك من قبل المستخدمين.
              </p>
            </section>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
// No logic needed for a static legal page
</script>

<style scoped>
.terms-page {
  background: linear-gradient(180deg, #f0f9fa 0%, #ffffff 100%);
  min-height: 100vh;
}

.vibrant-gradient-text {
  background: linear-gradient(135deg, #04809f 0%, #75b9c4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.lh-relaxed {
  line-height: 1.8 !important;
}

.glass-card {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(20px);
  border-radius: 32px !important;
  border: 1px solid rgba(4, 128, 159, 0.1) !important;
  box-shadow: 0 30px 60px -12px rgba(4, 128, 159, 0.05) !important;
}

.standard-list {
  padding-right: 24px;
  list-style-type: none;
}

.standard-list li {
  margin-bottom: 12px;
  position: relative;
}

.standard-list li::before {
  content: '•';
  color: #04809f;
  font-weight: bold;
  position: absolute;
  right: -20px;
}
</style>
