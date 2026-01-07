<template>
  <div class="page" dir="rtl">
    <!-- =================== NAV (مثل الصورة) =================== -->
    <header class="topbar">
      <div class="container topbar__inner">
        <!-- Left -->
        <div class="leftSide">
          <span class="profileLink"> <a href="/login">تسجيل الدخول</a></span>
        </div>

        <!-- Center -->
        <nav class="navCenter">
          <a class="navItem" href="#about">عن أتراب</a>

          <a class="navItem" href="/organizations">
            <svg
              class="navIcon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M3 21V8a2 2 0 012-2h14a2 2 0 012 2v13" />
              <path d="M7 21v-7h10v7" />
              <path d="M9 10h6" />
            </svg>
            الجامعات
          </a>
        </nav>
        <!-- Right spacer -->
        <div class="rightSpacer"></div>
      </div>
    </header>

    <!-- =================== HERO (مثل الصورة) =================== -->
    <section class="hero" id="universities">
      <div class="container hero__inner">
        <span class="heroPill">
          <span class="sparkle">✦</span>
          منصة التواصل التعليمية الأولى في المنطقة
        </span>

        <h1 class="hero__title">
          تواصل مع زملائك <br />
          في نفس المادة
        </h1>

        <p class="hero__subtitle">
          انضم إلى آلاف الطلاب الذين يبادلون المعرفة والموارد التعليمية في نفس الجامعة والكلية
          والمادة. تعلّم، شارك، وتميّز!
        </p>

        <div class="hero__cta">
          <button class="btn btn--primary"><a href="/register">ابدأ رحلتك الآن</a></button>
        </div>
      </div>
    </section>

    <!-- =================== WHY (Gradient bar) =================== -->
    <section class="band" id="resources">
      <div class="container band__inner">
        <h2 class="band__title">لماذا أتراب؟</h2>
        <p class="band__subtitle">نوفر لك كل ما تحتاجه للتواصل مع زملائك ومشاركة المعرفة</p>
      </div>
    </section>

    <!-- =================== FEATURES (2 rows × 3 cards) =================== -->
    <section class="section">
      <div class="container">
        <div class="cards">
          <article v-for="(f, i) in features" :key="i" class="card">
            <div class="card__iconWrap">
              <div class="card__icon" :style="{ background: f.bg }" aria-hidden="true">
                {{ f.icon }}
              </div>
            </div>

            <div class="card__title">{{ f.title }}</div>
            <p class="card__desc">{{ f.desc }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- =================== HOW IT WORKS =================== -->
    <section class="section how" id="courses">
      <div class="container">
        <div class="center">
          <h2 class="h2">كيف يعمل أتراب؟</h2>
          <p class="muted">ثلاث خطوات بسيطة للبدء</p>
        </div>

        <div class="howSteps">
          <div v-for="(s, i) in steps" :key="i" class="howStep">
            <div class="howStep__icon">
              {{ s.icon }}
              <span class="howStep__badge">{{ i + 1 }}</span>
            </div>
            <div class="howStep__title">{{ s.title }}</div>
            <p class="howStep__desc">{{ s.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== CTA (Gradient section) =================== -->
    <section class="cta">
      <div class="container cta__inner">
        <h2 class="cta__title">جاهز للبدء؟</h2>
        <p class="cta__subtitle">انضم إلى آلاف الطلاب الذين يستفيدون من أتراب كل يوم</p>

        <div class="cta__buttons">
          <button class="btn btn--light">سجّل الآن</button>
        </div>
      </div>
    </section>

    <!-- =================== Footer =================== -->
    <footer class="footer" id="about">
      <div class="container footer__grid">
        <div class="footerBrand">
          <div class="footerLogo">تخرج</div>
          <div>
            <div class="footerName">أتراب</div>
            <div class="footerDesc">
              منصة تواصل تعليمية تجمع الطلاب لنفس الجامعة والكلية والمادة لمشاركة المعرفة والموارد
              التعليمية.
            </div>
          </div>
        </div>

        <div>
          <div class="footerTitle">عن أتراب</div>
          <a class="footerLink" href="#about">عن المنصة</a>
          <a class="footerLink" href="#courses">كيف يعمل</a>
          <a class="footerLink" href="#resources">المزايا</a>
        </div>

        <div>
          <div class="footerTitle">الدعم</div>
          <a class="footerLink" href="#">سياسة الاستخدام</a>
        </div>

        <div>
          <div class="footerTitle">تواصل</div>
          <a class="footerLink" href="mailto:hello@atrab.com">البريد الإلكتروني</a>
        </div>
      </div>

      <div class="container footer__bottom">
        <span class="muted">© {{ year }} أتراب. جميع الحقوق محفوظة.</span>
      </div>

      <button class="floating" aria-label="مساعدة">🎓</button>
    </footer>
  </div>
</template>

<script setup>
const year = new Date().getFullYear()

const features = [
  {
    icon: '💬',
    bg: '#FFE7C6',
    title: 'نقاشات حيّة',
    desc: 'شارك في نقاشات المواد، اسأل واستفد، واحصل على إجابات من زملائك والمساعدين.',
  },
  {
    icon: '📄',
    bg: '#DDF5D9',
    title: 'موارد تعليمية',
    desc: 'احصل على ملخصات، ملفات PDF، وملاحظات من مشاركة الطلاب المتفوقين.',
  },
  {
    icon: '👥',
    bg: '#DCEEFF',
    title: 'تواصل مباشر',
    desc: 'تواصل مع زملائك في نفس الجامعة والكلية والمادة، وابدأ محادثات خاصة أو جماعية.',
  },
  {
    icon: '❤️',
    bg: '#FFE2EA',
    title: 'مجتمع داعم',
    desc: 'انضم لمجتمع من الطلاب المتحمسين الذين يدعمون بعضهم لتحقيق أفضل النتائج.',
  },
  {
    icon: '🛡️',
    bg: '#E6F4F6',
    title: 'آمن وخاص',
    desc: 'بياناتك محمية. نحترم الخصوصية والأمان بمعايير عالية.',
  },
  {
    icon: '🔎',
    bg: '#F0E7FF',
    title: 'بحث ذكي',
    desc: 'ابحث عن المواد والموارد والنقاشات بسهولة، ورتّب وقتك بذكاء.',
  },
]

const steps = [
  { icon: '🎓', title: 'اختر جامعتك', desc: 'ابدأ باختيار جامعتك من قائمة الجامعات المدعومة.' },
  { icon: '📘', title: 'اختر موادك', desc: 'حدد الكلية والمواد التي تدرسها لهذا الفصل.' },
  { icon: '🤝', title: 'تواصل وشارك', desc: 'ابدأ التواصل مع زملائك وشارك المعرفة والموارد.' },
]
</script>

<style scoped>
/* Base */
.page {
  background: #fff;
  color: #0f172a;
}
.container {
  width: min(1100px, 92%);
  margin: 0 auto;
}
.muted {
  color: #64748b;
}
.h2 {
  font-size: clamp(22px, 3vw, 32px);
  margin: 0;
}
.center {
  text-align: center;
}

/* =================== NAV =================== */
.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #fff;
  border-bottom: 1px solid #eef2f7;
}
.topbar__inner {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 18px 0;
}
.leftSide {
  display: flex;
  align-items: center;
  gap: 14px;
}
.profileLink {
  font-weight: 700;
}
.bellBtn {
  position: relative;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 6px;
  border-radius: 12px;
}
.bellBtn:hover {
  background: #f8fafc;
}
.bellIcon {
  width: 22px;
  height: 22px;
  color: #0f172a;
  opacity: 0.75;
}
.notifDot {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 9px;
  height: 9px;
  background: #0f6b7b;
  border: 2px solid #fff;
  border-radius: 999px;
}
.navCenter {
  display: flex;
  align-items: center;
  gap: 26px;
  justify-content: center;
}
.navItem {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #0f172a;
  text-decoration: none;
  font-weight: 600;
  padding: 10px 14px;
  border-radius: 18px;
}
.navItem:hover {
  background: #f8fafc;
}
.navIcon {
  width: 18px;
  height: 18px;
  opacity: 0.9;
}
.navItem.isActive {
  background: #fff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
  color: #0f6b7b;
}
.navItem.isActive .navIcon {
  color: #0f6b7b;
}
.rightSpacer {
  /* empty */
}

@media (max-width: 900px) {
  .navCenter {
    display: none;
  }
  .topbar__inner {
    grid-template-columns: 1fr;
  }
}

/* =================== HERO =================== */
.hero {
  padding: 70px 0 55px;
}
.hero__inner {
  text-align: center;
}
.heroPill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  border-radius: 999px;
  background: #e6f4f6;
  border: 1px solid rgba(15, 107, 123, 0.18);
  color: #0f6b7b;
  font-weight: 700;
}
.sparkle {
  font-size: 16px;
}
.hero__title {
  margin: 18px 0 12px;
  font-size: clamp(38px, 4.2vw, 62px);
  line-height: 1.1;
  letter-spacing: -0.4px;
}
.hero__subtitle {
  max-width: 720px;
  margin: 0 auto;
  color: #475569;
  line-height: 1.9;
  font-size: 15px;
}
.hero__cta {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
  flex-wrap: wrap;
}
.hero__badges {
  margin-top: 18px;
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}
.miniBadge {
  color: #0f172a;
  font-size: 13px;
  padding: 7px 12px;
  border-radius: 999px;
  background: #f8fafc;
  border: 1px solid #eef2f7;
}

/* Buttons */
.btn {
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 10px 16px;
  font-weight: 700;
  cursor: pointer;
  font-size: 14px;
}
.btn--primary {
  background: #0f6b7b;
  color: #fff;
}
.btn--outline {
  background: #fff;
  border-color: #0f6b7b;
  color: #0f6b7b;
}
.btn--light {
  background: #fff;
  color: #0b4d58;
}
.btn--ghostLight {
  background: rgba(255, 255, 255, 0.14);
  border-color: rgba(255, 255, 255, 0.22);
  color: #fff;
}

/* Band */
.band {
  background: linear-gradient(180deg, #3b90a0, #2f7f90);
  color: #fff;
  padding: 34px 0;
}
.band__inner {
  text-align: center;
}
.band__title {
  margin: 0;
  font-size: 28px;
}
.band__subtitle {
  margin: 8px 0 0;
  opacity: 0.92;
}

/* Cards */
.section {
  padding: 46px 0;
}
.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.card {
  background: #fff;
  border: 1px solid #eef2f7;
  border-radius: 16px;
  padding: 18px 16px;
  box-shadow: 0 6px 22px rgba(15, 23, 42, 0.06);
}
.card__iconWrap {
  margin-bottom: 10px;
}
.card__icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  font-size: 20px;
}
.card__title {
  font-weight: 900;
  margin-bottom: 8px;
}
.card__desc {
  margin: 0;
  color: #64748b;
  line-height: 1.75;
  font-size: 14px;
}

@media (max-width: 900px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 520px) {
  .cards {
    grid-template-columns: 1fr;
  }
}

/* How */
.how {
  padding-top: 32px;
}
.howSteps {
  margin-top: 26px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.howStep {
  text-align: center;
  padding: 10px 8px;
}
.howStep__icon {
  width: 62px;
  height: 62px;
  margin: 0 auto 12px;
  border-radius: 18px;
  background: #2f7f90;
  color: #fff;
  display: grid;
  place-items: center;
  font-size: 24px;
  position: relative;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.12);
}
.howStep__badge {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 26px;
  height: 26px;
  border-radius: 999px;
  background: #fff;
  color: #0f6b7b;
  border: 1px solid #e2e8f0;
  font-weight: 900;
  display: grid;
  place-items: center;
  font-size: 12px;
}
.howStep__title {
  font-weight: 900;
  margin-bottom: 8px;
}
.howStep__desc {
  margin: 0;
  color: #64748b;
  line-height: 1.75;
  font-size: 14px;
}
@media (max-width: 900px) {
  .howSteps {
    grid-template-columns: 1fr;
  }
}

/* CTA */
.cta {
  background: linear-gradient(180deg, #3b90a0, #2f7f90);
  color: #fff;
  padding: 56px 0;
}
.cta__inner {
  text-align: center;
}
.cta__title {
  margin: 0;
  font-size: 34px;
}
.cta__subtitle {
  margin: 10px 0 0;
  opacity: 0.9;
}
.cta__buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 18px;
  flex-wrap: wrap;
}
.cta__mini {
  margin-top: 18px;
  display: flex;
  justify-content: center;
  gap: 18px;
  flex-wrap: wrap;
}
.ctaMini {
  font-size: 13px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

/* Footer */
.footer {
  padding: 34px 0 16px;
  background: #fff;
}
.footer__grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1fr;
  gap: 18px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eef2f7;
}
.footerBrand {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.footerLogo {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #e6f4f6;
  color: #0f6b7b;
  font-weight: 900;
}
.footerName {
  font-weight: 900;
  margin-bottom: 4px;
}
.footerDesc {
  color: #64748b;
  font-size: 14px;
  line-height: 1.7;
  max-width: 360px;
}
.footerTitle {
  font-weight: 900;
  margin-bottom: 10px;
}
.footerLink {
  display: block;
  color: #475569;
  text-decoration: none;
  margin: 8px 0;
  font-size: 14px;
}
.footerLink:hover {
  color: #0f6b7b;
}
.footer__bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding-top: 14px;
}
@media (max-width: 900px) {
  .footer__grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 520px) {
  .footer__grid {
    grid-template-columns: 1fr;
  }
}

/* Floating button */
.floating {
  position: fixed;
  left: 18px;
  bottom: 18px;
  width: 52px;
  height: 52px;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  background: #fff;
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.16);
  cursor: pointer;
  font-size: 20px;
}

a {
  text-decoration: none;
}
</style>
