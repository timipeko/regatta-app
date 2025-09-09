
import { createApp, ref, onMounted } from "vue";

declare global { interface Window { __API__?: string } }

const api = (p: string) => `${(window as any).__API__ || (import.meta as any).env?.VITE_API_BASE || "https://regatta-api.fly.dev/api"}${p}`;

const App = {
  setup() {
    const regattas = ref<any[]>([]);
    const selected = ref<any|null>(null);
    const classes = ref<any[]>([]);
    const races = ref<any[]>([]);
    const standings = ref<any[]>([]);
    const error = ref<string>("");

    const loadRegattas = async () => {
      try {
        error.value = "";
        const r = await fetch(api("/regattas/"));
        regattas.value = await r.json();
      } catch (e:any) { error.value = String(e.message); }
    };
    const loadClasses = async (regattaId: number) => {
      const r = await fetch(api(`/regattas/${regattaId}/classes/`));
      classes.value = await r.json();
    };
    const loadRaces = async (regattaClassId: number) => {
      const r = await fetch(api(`/regatta-classes/${regattaClassId}/races/`));
      races.value = await r.json();
    };
    const loadStandings = async (regattaClassId: number) => {
      const r = await fetch(api(`/regatta-classes/${regattaClassId}/standings/`));
      standings.value = await r.json();
    };

    onMounted(loadRegattas);

    return { regattas, selected, classes, races, standings, error, loadClasses, loadRaces, loadStandings };
  },
  template: `
    <main style="font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 24px; max-width: 1100px; margin: 0 auto;">
      <h1 style="margin: 0 0 12px;">⛵ Regatta — Tulospalvelu</h1>
      <p v-if="error" style="color:#b00;">Virhe: {{ error }}</p>

      <div style="display:grid; grid-template-columns: 1fr 2fr; gap: 16px;">
        <section style="background:#fff; border:1px solid #eee; border-radius:12px; padding:16px;">
          <h2 style="margin-top:0;">Regatat</h2>
          <div v-if="regattas.length===0">Ei regattoja.</div>
          <ul style="padding:0; list-style:none;">
            <li v-for="r in regattas" :key="r.id" style="margin-bottom:8px;">
              <button @click="selected=r; loadClasses(r.id)" style="cursor:pointer;">{{ r.name }}</button>
              <span style="color:#666; margin-left:8px;">{{ r.start_date }} → {{ r.end_date }}</span>
            </li>
          </ul>
        </section>

        <section style="background:#fff; border:1px solid #eee; border-radius:12px; padding:16px;">
          <div v-if="!selected">Valitse regatta vasemmalta.</div>
          <div v-else>
            <h2 style="margin-top:0;">{{ selected.name }}</h2>
            <h3>Luokat</h3>
            <div style="display:flex; gap:12px; flex-wrap:wrap;">
              <div v-for="c in classes" :key="c.id" style="border:1px solid #eee; border-radius:12px; padding:12px; min-width:220px;">
                <strong>{{ c.name }}</strong>
                <div style="color:#666; font-size:12px;">Handicap: {{ c.handicap_system }} — Scoring: {{ c.scoring_system }}</div>
                <div style="margin-top:8px;">
                  <button @click="loadRaces(c.id)" style="margin-right:8px;">Lähdöt</button>
                  <button @click="loadStandings(c.id)">Yhteispisteet</button>
                </div>
              </div>
            </div>

            <div v-if="races.length">
              <h3 style="margin-top:16px;">Lähdöt</h3>
              <div v-for="race in races" :key="race.id" style="border-top:1px solid #eee; padding-top:8px; margin-top:8px;">
                <strong>Lähtö #{{ race.sequence }}</strong> — {{ race.date }}
              </div>
            </div>

            <div v-if="standings.length">
              <h3 style="margin-top:16px;">Yhteispisteet</h3>
              <table style="width:100%; border-collapse: collapse;">
                <thead>
                  <tr>
                    <th style="text-align:left; border-bottom:1px solid #eee; padding:6px;">Vene</th>
                    <th style="text-align:left; border-bottom:1px solid #eee; padding:6px;">Purjenro</th>
                    <th style="text-align:left; border-bottom:1px solid #eee; padding:6px;">Pisteet</th>
                    <th style="text-align:left; border-bottom:1px solid #eee; padding:6px;">Sijat</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in standings" :key="row.entry_id">
                    <td style="padding:6px;">{{ row.boat.name }}</td>
                    <td style="padding:6px;">{{ row.boat.sail_number }}</td>
                    <td style="padding:6px;">{{ row.total_points }}</td>
                    <td style="padding:6px;">{{ (row.ranks || []).filter(Boolean).join(', ') }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>
        </section>
      </div>
    </main>
  `
};

createApp(App).mount("#app");
