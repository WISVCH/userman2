Vue.component('dienst2', {
    props: ['status', 'full_name'],
    template: `
      <div>
        <span v-if="status.error">
            <small>{{ status.error }}</small>
        </span>
        <span v-if="status.status == 'error'">
            <i class="fas fa-times-circle" style="color: red;"></i>
            <a v-bind:href="'https://dienst2.ch.tudelft.nl/ldb/index/#' + encodeURIComponent(full_name)">
                {{ status.message }}
            </a>
        </span>
        <span v-if="status.status == 'warning'">
            <i class="fas fa-exclamation-circle" style="color: orange"></i>
            <a v-bind:href="status.href">{{ status.message }}</a>
        </span>
        <span v-if="status.status == 'success'">
            <i class="fas fa-check-circle" style="color: green;"></i>
            <a v-bind:href="status.href">{{ status.message }}</a>
        </span>
        <span v-if="status.status == 'whitelisted'">
            <i class="fas fa-check-circle" style="color: green;"></i>
            {{ status.message }}
        </span>
      </div>
    `
})

Vue.component('actions', {
    props: ['dn', 'children'],
    data: function () {
        return {
            actions: undefined,
        }
    },
    async created() {
        if (this.children) {
            this.actions = this.children;
        } else {
            this.fetchActions(this.dn);
            setInterval(this.fetchActions, 10_000)
        }
    },
    methods: {
        async fetchActions() {
            let query = '';
            if (this.dn) {
                query = '?dn=' + encodeURIComponent(this.dn);
            }
            const actions = await fetch('/actions/actions.json' + query);
            this.actions = (await actions.json()).actions;
        }
    },
    template: `
      <ul v-if="this.actions && this.actions.length" class="actions">
        <li v-for="a in actions" :key="a.dn">
            <i v-if="a.locked" class="fas fa-lock" style="color: red"></i>
            <i v-else class="fas fa-unlock" style="color: green"></i>
            {{ a.description }}
             <actions v-if="a.children.length" :children="a.children"></actions>
        </li>
      </ul>
      <span v-else-if="this.actions">No pending actions</span>
      <span v-else><i class="fas fa-sync-alt spinner"></i></a></span>
    `
})
