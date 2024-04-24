<template>
  <div
    class="d-flex align-center justify-space-between justify-md-end flex-wrap gap"
  >
    <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
    <v-chip dense color="success">
      <v-chip small dense class="mr-2" color="green darken-3 white--text"
        >26</v-chip
      >
      von 30 anwesend
    </v-chip>
    <v-chip dense color="warning">
      <v-chip small dense class="mr-2" color="orange darken-3 white--text"
        >3</v-chip
      >
      entschuldigt
    </v-chip>
    <v-chip dense color="error">
      <v-chip small dense class="mr-2" color="red darken-3 white--text"
        >1</v-chip
      >
      unentschuldigt
    </v-chip>
    <v-chip dense color="grey lighten-1">
      <v-chip small dense class="mr-2" color="grey darken-1 white--text"
        >4</v-chip
      >
      Hausaufgaben vergessen
    </v-chip>
    <v-chip dense color="primary" outlined>
      <v-icon>$edit</v-icon>
    </v-chip>
    <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
  </div>
</template>

<script>
import documentationPartMixin from "./documentationPartMixin";

export default {
  name: "LessonNotes",
  mixins: [documentationPartMixin],
};
</script>

<style scoped>
.gap {
  gap: 0.25em;
}
</style>
