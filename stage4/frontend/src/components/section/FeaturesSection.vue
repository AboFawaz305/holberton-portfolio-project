<template>
  <v-container class="section-padding overflow-visible">
    <div class="text-center mb-16" data-aos="fade-up">
      <v-chip color="primary" variant="tonal" class="mb-4 font-weight-bold px-6"
        >لماذا أتراب؟</v-chip
      >
      <h2 class="text-h3 font-weight-black mb-4">
        المميزات التي تجعلنا <span class="brand-gradient-text">مختلفين</span>
      </h2>
    </div>

    <v-row align="center" class="mb-16 pb-12">
      <v-col cols="12" md="6" data-aos="fade-right">
        <div class="feature-visual-wrapper">
          <div class="feature-blob bg-teal-brand"></div>
          <div class="glass-card feature-mockup main-card">
            <div class="chat-sim-detailed pa-4">
              <div class="skeleton-avatar mb-4"></div>
              <div class="skeleton-line w-75 mb-2"></div>
              <div class="skeleton-line w-50 mb-6"></div>
              <div class="floating-badge-ui glass-card">نقاش حي الآن</div>
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="text-right" data-aos="fade-left">
        <h3 class="text-h4 font-weight-bold mb-6">نقاشات حية ومباشرة</h3>
        <p class="text-h6 text-grey-darken-1 lh-relaxed font-weight-regular">
          لا تنتظر الإجابة لساعات. انضم لمجموعات النقاش الحية لموادك، اسأل زملائك، وتبادل الخبرات في
          الوقت الفعلي مع طلاب يدرسون نفس المنهج.
        </p>
      </v-col>
    </v-row>

    <v-row align="center" class="mb-16 pb-12">
      <v-col cols="12" md="6" class="text-right order-last order-md-first" data-aos="fade-right">
        <h3 class="text-h4 font-weight-bold mb-6">مكتبة موارد ذكية</h3>
        <p class="text-h6 text-grey-darken-1 lh-relaxed font-weight-regular">
          وداعاً لضياع الملفات في مجموعات الواتساب. كل الملخصات، أسئلة السنوات السابقة، وشروحات
          المواد منظمة ومتاحة للجميع في مكان واحد. بفضل نظام التصويت، تظهر لك أفضل المصادر دائماً في
          القمة.
        </p>
      </v-col>
      <v-col cols="12" md="6" data-aos="fade-left">
        <div class="feature-visual-wrapper">
          <div class="feature-blob bg-blue-accent"></div>
          <div class="glass-card feature-mockup secondary-card">
            <div class="resource-sim pa-6">
              <div class="d-flex align-center mb-6">
                <div class="d-flex flex-column align-center me-4 voting-ui">
                  <v-icon color="primary" size="small">mdi-arrow-up-bold</v-icon>
                  <span class="text-caption font-weight-black text-primary my-n1">42</span>
                  <v-icon color="grey-lighten-1" size="small">mdi-arrow-down-bold</v-icon>
                </div>
                <div class="flex-grow-1">
                  <v-icon color="primary" class="mb-1" size="small">mdi-file-pdf-box</v-icon>
                  <div class="skeleton-line w-75 mb-0" style="height: 8px"></div>
                </div>
              </div>

              <div class="d-flex align-center opacity-60">
                <div class="d-flex flex-column align-center me-4 voting-ui">
                  <v-icon color="grey-lighten-1" size="small">mdi-arrow-up-bold</v-icon>
                  <span class="text-caption font-weight-bold text-grey my-n1">12</span>
                  <v-icon color="grey-lighten-1" size="small">mdi-arrow-down-bold</v-icon>
                </div>
                <div class="flex-grow-1">
                  <v-icon color="grey" class="mb-1" size="small">mdi-file-document-outline</v-icon>
                  <div class="skeleton-line w-50 mb-0" style="height: 8px"></div>
                </div>
              </div>
            </div>
            <div class="floating-badge-ui glass-card vote-badge">
              <v-icon color="primary" class="me-2" size="small">mdi-trending-up</v-icon>
              <span>الأكثر فائدة</span>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <v-row align="center">
      <v-col cols="12" md="6" data-aos="fade-right">
        <div class="feature-visual-wrapper">
          <div class="feature-blob bg-teal-dark"></div>
          <div class="glass-card feature-mockup tertiary-card">
            <div class="community-sim d-flex justify-center align-center h-100">
              <div class="d-flex justify-center align-center avatar-stack">
                <v-avatar
                  v-for="n in 4"
                  :key="n"
                  color="primary"
                  class="avatar-item border-white"
                  size="50"
                >
                  <v-icon color="white">mdi-account-circle</v-icon>
                </v-avatar>
              </div>
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="text-right" data-aos="fade-left">
        <h3 class="text-h4 font-weight-bold mb-6">مجتمع أكاديمي داعم</h3>
        <p class="text-h6 text-grey-darken-1 lh-relaxed font-weight-regular">
          ابنِ شبكة علاقاتك مع طلاب كليتك وجامعتك. تواصل مع المتميزين، كون مجموعات دراسية، وساهم في
          مساعدة غيرك لتحقيق أفضل النتائج.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.brand-gradient-text {
  background: linear-gradient(135deg, #04809f, #75b9c4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.lh-relaxed {
  line-height: 1.8 !important;
}

/* Visual Components Wrapper */
.feature-visual-wrapper {
  position: relative;
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feature-blob {
  position: absolute;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
  z-index: 1;
}
.bg-teal-brand {
  background: #04809f;
}
.bg-blue-accent {
  background: #75b9c4;
}
.bg-teal-dark {
  background: #025a70;
}

.feature-mockup {
  width: 320px;
  height: 220px;
  border-radius: 28px;
  z-index: 2;
  position: relative;
}

.main-card {
  transform: rotate(-5deg);
}
.secondary-card {
  transform: rotate(5deg);
}
.tertiary-card {
  transform: scale(1.05);
}

.skeleton-line {
  height: 10px;
  background: #e0e6ed;
  border-radius: 5px;
}
.skeleton-avatar {
  width: 40px;
  height: 40px;
  background: #04809f15;
  border-radius: 12px;
}

/* Voting UI Mockup */
.voting-ui {
  background: rgba(255, 255, 255, 0.5);
  padding: 4px;
  border-radius: 8px;
  min-width: 32px;
}

/* Floating Badge */
.floating-badge-ui {
  position: absolute;
  padding: 12px 20px;
  border-radius: 16px;
  font-weight: 800;
  font-size: 13px;
  color: #04809f;
  box-shadow: 0 15px 30px rgba(4, 128, 159, 0.1) !important;
}
.vote-badge {
  top: -25px;
  right: -25px;
  background: white !important;
}

/* Avatar Overlap Fix */
.avatar-stack {
  direction: ltr; /* Ensures overlap goes the same way for everyone */
}
.avatar-item {
  margin-left: -15px; /* Creates the overlap */
  border: 3px solid white !important;
}

.feature-visual-wrapper:hover .feature-mockup {
  transform: rotate(0) scale(1.1);
  transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
</style>
