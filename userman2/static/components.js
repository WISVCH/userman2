Vue.component('dienst2', {
    props: ['status', 'full_name'],
    template: `
      <div>
        <span v-if="status.error">
            <small>{{ status.error }}</small>
        </span>
        <span v-if="status.status == 'error'">
            <i class="fas fa-times-circle" style="color: red;"></i>
            <a v-bind:href="'https://dienst2.chnet/ldb/index/#' + full_name">{{ status.message }}</a>
        </span>
        <span v-if="status.status == 'warning'">
            <i class="fas fa-exclamation-circle" style="color: orange"></i>
            <a v-bind:href="status.href">{{ status.message }}</a>
        </span>
        <span v-if="status.status == 'success'">
            <i class="fas fa-check-circle" style="color: green;"></i>
            <a v-bind:href="status.href">{{ status.message }}</a>
        </span>
      </div>
    `
  })
