const {
  SvelteComponent: jt,
  assign: Bt,
  create_slot: Dt,
  detach: At,
  element: Et,
  get_all_dirty_from_scope: Tt,
  get_slot_changes: Xt,
  get_spread_update: Yt,
  init: Gt,
  insert: Ot,
  safe_not_equal: Rt,
  set_dynamic_element_data: Be,
  set_style: z,
  toggle_class: D,
  transition_in: bt,
  transition_out: gt,
  update_slot_base: Ht
} = window.__gradio__svelte__internal;
function Jt(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = Dt(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let a = 0; a < s.length; a += 1)
    r = Bt(r, s[a]);
  return {
    c() {
      e = Et(
        /*tag*/
        n[14]
      ), f && f.c(), Be(
        /*tag*/
        n[14]
      )(e, r), D(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), D(
        e,
        "padded",
        /*padding*/
        n[6]
      ), D(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), D(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), D(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), z(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), z(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), z(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), z(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), z(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), z(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), z(e, "border-width", "var(--block-border-width)");
    },
    m(a, o) {
      Ot(a, e, o), f && f.m(e, null), l = !0;
    },
    p(a, o) {
      f && f.p && (!l || o & /*$$scope*/
      131072) && Ht(
        f,
        i,
        a,
        /*$$scope*/
        a[17],
        l ? Xt(
          i,
          /*$$scope*/
          a[17],
          o,
          null
        ) : Tt(
          /*$$scope*/
          a[17]
        ),
        null
      ), Be(
        /*tag*/
        a[14]
      )(e, r = Yt(s, [
        (!l || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!l || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!l || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), D(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), D(
        e,
        "padded",
        /*padding*/
        a[6]
      ), D(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), D(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), D(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), o & /*height*/
      1 && z(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), o & /*width*/
      2 && z(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), o & /*variant*/
      16 && z(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), o & /*allow_overflow*/
      2048 && z(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && z(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), o & /*min_width*/
      8192 && z(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      l || (bt(f, a), l = !0);
    },
    o(a) {
      gt(f, a), l = !1;
    },
    d(a) {
      a && At(e), f && f.d(a);
    }
  };
}
function Kt(n) {
  let e, t = (
    /*tag*/
    n[14] && Jt(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (bt(t, l), e = !0);
    },
    o(l) {
      gt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Qt(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: a = [] } = e, { variant: o = "solid" } = e, { border_mode: _ = "base" } = e, { padding: c = !0 } = e, { type: d = "normal" } = e, { test_id: u = void 0 } = e, { explicit_call: h = !1 } = e, { container: C = !0 } = e, { visible: k = !0 } = e, { allow_overflow: F = !0 } = e, { scale: g = null } = e, { min_width: m = 0 } = e, b = d === "fieldset" ? "fieldset" : "div";
  const B = (y) => {
    if (y !== void 0) {
      if (typeof y == "number")
        return y + "px";
      if (typeof y == "string")
        return y;
    }
  };
  return n.$$set = (y) => {
    "height" in y && t(0, f = y.height), "width" in y && t(1, s = y.width), "elem_id" in y && t(2, r = y.elem_id), "elem_classes" in y && t(3, a = y.elem_classes), "variant" in y && t(4, o = y.variant), "border_mode" in y && t(5, _ = y.border_mode), "padding" in y && t(6, c = y.padding), "type" in y && t(16, d = y.type), "test_id" in y && t(7, u = y.test_id), "explicit_call" in y && t(8, h = y.explicit_call), "container" in y && t(9, C = y.container), "visible" in y && t(10, k = y.visible), "allow_overflow" in y && t(11, F = y.allow_overflow), "scale" in y && t(12, g = y.scale), "min_width" in y && t(13, m = y.min_width), "$$scope" in y && t(17, i = y.$$scope);
  }, [
    f,
    s,
    r,
    a,
    o,
    _,
    c,
    u,
    h,
    C,
    k,
    F,
    g,
    m,
    b,
    B,
    d,
    i,
    l
  ];
}
class Ut extends jt {
  constructor(e) {
    super(), Gt(this, e, Qt, Kt, Rt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Wt,
  attr: xt,
  create_slot: $t,
  detach: el,
  element: tl,
  get_all_dirty_from_scope: ll,
  get_slot_changes: nl,
  init: il,
  insert: fl,
  safe_not_equal: sl,
  transition_in: ol,
  transition_out: al,
  update_slot_base: rl
} = window.__gradio__svelte__internal;
function _l(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = $t(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = tl("div"), i && i.c(), xt(e, "class", "svelte-1hnfib2");
    },
    m(f, s) {
      fl(f, e, s), i && i.m(e, null), t = !0;
    },
    p(f, [s]) {
      i && i.p && (!t || s & /*$$scope*/
      1) && rl(
        i,
        l,
        f,
        /*$$scope*/
        f[0],
        t ? nl(
          l,
          /*$$scope*/
          f[0],
          s,
          null
        ) : ll(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (ol(i, f), t = !0);
    },
    o(f) {
      al(i, f), t = !1;
    },
    d(f) {
      f && el(e), i && i.d(f);
    }
  };
}
function ul(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, l];
}
class cl extends Wt {
  constructor(e) {
    super(), il(this, e, ul, _l, sl, {});
  }
}
const {
  SvelteComponent: dl,
  attr: De,
  check_outros: ml,
  create_component: bl,
  create_slot: gl,
  destroy_component: hl,
  detach: de,
  element: wl,
  empty: kl,
  get_all_dirty_from_scope: pl,
  get_slot_changes: vl,
  group_outros: yl,
  init: ql,
  insert: me,
  mount_component: Cl,
  safe_not_equal: Fl,
  set_data: Ll,
  space: Sl,
  text: zl,
  toggle_class: U,
  transition_in: se,
  transition_out: be,
  update_slot_base: Ml
} = window.__gradio__svelte__internal;
function Ae(n) {
  let e, t;
  return e = new cl({
    props: {
      $$slots: { default: [Vl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      bl(e.$$.fragment);
    },
    m(l, i) {
      Cl(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (se(e.$$.fragment, l), t = !0);
    },
    o(l) {
      be(e.$$.fragment, l), t = !1;
    },
    d(l) {
      hl(e, l);
    }
  };
}
function Vl(n) {
  let e;
  return {
    c() {
      e = zl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      me(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Ll(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && de(e);
    }
  };
}
function Nl(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[2].default
  ), s = gl(
    f,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && Ae(n)
  );
  return {
    c() {
      e = wl("span"), s && s.c(), t = Sl(), r && r.c(), l = kl(), De(e, "data-testid", "block-info"), De(e, "class", "svelte-22c38v"), U(e, "sr-only", !/*show_label*/
      n[0]), U(e, "hide", !/*show_label*/
      n[0]), U(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(a, o) {
      me(a, e, o), s && s.m(e, null), me(a, t, o), r && r.m(a, o), me(a, l, o), i = !0;
    },
    p(a, [o]) {
      s && s.p && (!i || o & /*$$scope*/
      8) && Ml(
        s,
        f,
        a,
        /*$$scope*/
        a[3],
        i ? vl(
          f,
          /*$$scope*/
          a[3],
          o,
          null
        ) : pl(
          /*$$scope*/
          a[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && U(e, "sr-only", !/*show_label*/
      a[0]), (!i || o & /*show_label*/
      1) && U(e, "hide", !/*show_label*/
      a[0]), (!i || o & /*info*/
      2) && U(
        e,
        "has-info",
        /*info*/
        a[1] != null
      ), /*info*/
      a[1] ? r ? (r.p(a, o), o & /*info*/
      2 && se(r, 1)) : (r = Ae(a), r.c(), se(r, 1), r.m(l.parentNode, l)) : r && (yl(), be(r, 1, 1, () => {
        r = null;
      }), ml());
    },
    i(a) {
      i || (se(s, a), se(r), i = !0);
    },
    o(a) {
      be(s, a), be(r), i = !1;
    },
    d(a) {
      a && (de(e), de(t), de(l)), s && s.d(a), r && r.d(a);
    }
  };
}
function Pl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: s = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, s = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, s, l, i];
}
class Il extends dl {
  constructor(e) {
    super(), ql(this, e, Pl, Nl, Fl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Zl,
  append: qe,
  attr: T,
  bubble: jl,
  create_component: Bl,
  destroy_component: Dl,
  detach: ht,
  element: Ce,
  init: Al,
  insert: wt,
  listen: El,
  mount_component: Tl,
  safe_not_equal: Xl,
  set_data: Yl,
  set_style: W,
  space: Gl,
  text: Ol,
  toggle_class: S,
  transition_in: Rl,
  transition_out: Hl
} = window.__gradio__svelte__internal;
function Ee(n) {
  let e, t;
  return {
    c() {
      e = Ce("span"), t = Ol(
        /*label*/
        n[1]
      ), T(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      wt(l, e, i), qe(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && Yl(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && ht(e);
    }
  };
}
function Jl(n) {
  let e, t, l, i, f, s, r, a = (
    /*show_label*/
    n[2] && Ee(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Ce("button"), a && a.c(), t = Gl(), l = Ce("div"), Bl(i.$$.fragment), T(l, "class", "svelte-1lrphxw"), S(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), S(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), S(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], T(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), T(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), T(
        e,
        "title",
        /*label*/
        n[1]
      ), T(e, "class", "svelte-1lrphxw"), S(
        e,
        "pending",
        /*pending*/
        n[3]
      ), S(
        e,
        "padded",
        /*padded*/
        n[5]
      ), S(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), S(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), W(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), W(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), W(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(o, _) {
      wt(o, e, _), a && a.m(e, null), qe(e, t), qe(e, l), Tl(i, l, null), f = !0, s || (r = El(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), s = !0);
    },
    p(o, [_]) {
      /*show_label*/
      o[2] ? a ? a.p(o, _) : (a = Ee(o), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!f || _ & /*size*/
      16) && S(
        l,
        "small",
        /*size*/
        o[4] === "small"
      ), (!f || _ & /*size*/
      16) && S(
        l,
        "large",
        /*size*/
        o[4] === "large"
      ), (!f || _ & /*size*/
      16) && S(
        l,
        "medium",
        /*size*/
        o[4] === "medium"
      ), (!f || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      o[7]), (!f || _ & /*label*/
      2) && T(
        e,
        "aria-label",
        /*label*/
        o[1]
      ), (!f || _ & /*hasPopup*/
      256) && T(
        e,
        "aria-haspopup",
        /*hasPopup*/
        o[8]
      ), (!f || _ & /*label*/
      2) && T(
        e,
        "title",
        /*label*/
        o[1]
      ), (!f || _ & /*pending*/
      8) && S(
        e,
        "pending",
        /*pending*/
        o[3]
      ), (!f || _ & /*padded*/
      32) && S(
        e,
        "padded",
        /*padded*/
        o[5]
      ), (!f || _ & /*highlight*/
      64) && S(
        e,
        "highlight",
        /*highlight*/
        o[6]
      ), (!f || _ & /*transparent*/
      512) && S(
        e,
        "transparent",
        /*transparent*/
        o[9]
      ), _ & /*disabled, _color*/
      4224 && W(e, "color", !/*disabled*/
      o[7] && /*_color*/
      o[12] ? (
        /*_color*/
        o[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && W(e, "--bg-color", /*disabled*/
      o[7] ? "auto" : (
        /*background*/
        o[10]
      )), _ & /*offset*/
      2048 && W(
        e,
        "margin-left",
        /*offset*/
        o[11] + "px"
      );
    },
    i(o) {
      f || (Rl(i.$$.fragment, o), f = !0);
    },
    o(o) {
      Hl(i.$$.fragment, o), f = !1;
    },
    d(o) {
      o && ht(e), a && a.d(), Dl(i), s = !1, r();
    }
  };
}
function Kl(n, e, t) {
  let l, { Icon: i } = e, { label: f = "" } = e, { show_label: s = !1 } = e, { pending: r = !1 } = e, { size: a = "small" } = e, { padded: o = !0 } = e, { highlight: _ = !1 } = e, { disabled: c = !1 } = e, { hasPopup: d = !1 } = e, { color: u = "var(--block-label-text-color)" } = e, { transparent: h = !1 } = e, { background: C = "var(--background-fill-primary)" } = e, { offset: k = 0 } = e;
  function F(g) {
    jl.call(this, n, g);
  }
  return n.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, f = g.label), "show_label" in g && t(2, s = g.show_label), "pending" in g && t(3, r = g.pending), "size" in g && t(4, a = g.size), "padded" in g && t(5, o = g.padded), "highlight" in g && t(6, _ = g.highlight), "disabled" in g && t(7, c = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, u = g.color), "transparent" in g && t(9, h = g.transparent), "background" in g && t(10, C = g.background), "offset" in g && t(11, k = g.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = _ ? "var(--color-accent)" : u);
  }, [
    i,
    f,
    s,
    r,
    a,
    o,
    _,
    c,
    d,
    h,
    C,
    k,
    l,
    u,
    F
  ];
}
class Ql extends Zl {
  constructor(e) {
    super(), Al(this, e, Kl, Jl, Xl, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Ul,
  append: pe,
  attr: N,
  detach: Wl,
  init: xl,
  insert: $l,
  noop: ve,
  safe_not_equal: en,
  set_style: A,
  svg_element: _e
} = window.__gradio__svelte__internal;
function tn(n) {
  let e, t, l, i;
  return {
    c() {
      e = _e("svg"), t = _e("g"), l = _e("path"), i = _e("path"), N(l, "d", "M18,6L6.087,17.913"), A(l, "fill", "none"), A(l, "fill-rule", "nonzero"), A(l, "stroke-width", "2px"), N(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), N(i, "d", "M4.364,4.364L19.636,19.636"), A(i, "fill", "none"), A(i, "fill-rule", "nonzero"), A(i, "stroke-width", "2px"), N(e, "width", "100%"), N(e, "height", "100%"), N(e, "viewBox", "0 0 24 24"), N(e, "version", "1.1"), N(e, "xmlns", "http://www.w3.org/2000/svg"), N(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), N(e, "xml:space", "preserve"), N(e, "stroke", "currentColor"), A(e, "fill-rule", "evenodd"), A(e, "clip-rule", "evenodd"), A(e, "stroke-linecap", "round"), A(e, "stroke-linejoin", "round");
    },
    m(f, s) {
      $l(f, e, s), pe(e, t), pe(t, l), pe(e, i);
    },
    p: ve,
    i: ve,
    o: ve,
    d(f) {
      f && Wl(e);
    }
  };
}
class ln extends Ul {
  constructor(e) {
    super(), xl(this, e, null, tn, en, {});
  }
}
const nn = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Te = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
nn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Te[e][t],
      secondary: Te[e][l]
    }
  }),
  {}
);
function $(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function ge() {
}
function fn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const kt = typeof window < "u";
let Xe = kt ? () => window.performance.now() : () => Date.now(), pt = kt ? (n) => requestAnimationFrame(n) : ge;
const te = /* @__PURE__ */ new Set();
function vt(n) {
  te.forEach((e) => {
    e.c(n) || (te.delete(e), e.f());
  }), te.size !== 0 && pt(vt);
}
function sn(n) {
  let e;
  return te.size === 0 && pt(vt), {
    promise: new Promise((t) => {
      te.add(e = { c: n, f: t });
    }),
    abort() {
      te.delete(e);
    }
  };
}
const x = [];
function on(n, e = ge) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (fn(n, r) && (n = r, t)) {
      const a = !x.length;
      for (const o of l)
        o[1](), x.push(o, n);
      if (a) {
        for (let o = 0; o < x.length; o += 2)
          x[o][0](x[o + 1]);
        x.length = 0;
      }
    }
  }
  function f(r) {
    i(r(n));
  }
  function s(r, a = ge) {
    const o = [r, a];
    return l.add(o), l.size === 1 && (t = e(i, f) || ge), r(n), () => {
      l.delete(o), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function Ye(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Fe(n, e, t, l) {
  if (typeof t == "number" || Ye(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, r = n.opts.damping * f, a = (s - r) * n.inv_mass, o = (f + a) * n.dt;
    return Math.abs(o) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Ye(t) ? new Date(t.getTime() + o) : t + o);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Fe(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Fe(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Ge(n, e = {}) {
  const t = on(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, r, a, o = n, _ = n, c = 1, d = 0, u = !1;
  function h(k, F = {}) {
    _ = k;
    const g = a = {};
    return n == null || F.hard || C.stiffness >= 1 && C.damping >= 1 ? (u = !0, s = Xe(), o = k, t.set(n = _), Promise.resolve()) : (F.soft && (d = 1 / ((F.soft === !0 ? 0.5 : +F.soft) * 60), c = 0), r || (s = Xe(), u = !1, r = sn((m) => {
      if (u)
        return u = !1, r = null, !1;
      c = Math.min(c + d, 1);
      const b = {
        inv_mass: c,
        opts: C,
        settled: !0,
        dt: (m - s) * 60 / 1e3
      }, B = Fe(b, o, n, _);
      return s = m, o = n, t.set(n = B), b.settled && (r = null), !b.settled;
    })), new Promise((m) => {
      r.promise.then(() => {
        g === a && m();
      });
    }));
  }
  const C = {
    set: h,
    update: (k, F) => h(k(_, n), F),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return C;
}
const {
  SvelteComponent: an,
  append: P,
  attr: q,
  component_subscribe: Oe,
  detach: rn,
  element: _n,
  init: un,
  insert: cn,
  noop: Re,
  safe_not_equal: dn,
  set_style: ue,
  svg_element: I,
  toggle_class: He
} = window.__gradio__svelte__internal, { onMount: mn } = window.__gradio__svelte__internal;
function bn(n) {
  let e, t, l, i, f, s, r, a, o, _, c, d;
  return {
    c() {
      e = _n("div"), t = I("svg"), l = I("g"), i = I("path"), f = I("path"), s = I("path"), r = I("path"), a = I("g"), o = I("path"), _ = I("path"), c = I("path"), d = I("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(f, "fill", "#FF7C00"), q(f, "class", "svelte-43sxxs"), q(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(s, "fill", "#FF7C00"), q(s, "fill-opacity", "0.4"), q(s, "class", "svelte-43sxxs"), q(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(r, "fill", "#FF7C00"), q(r, "class", "svelte-43sxxs"), ue(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), q(o, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(o, "fill", "#FF7C00"), q(o, "fill-opacity", "0.4"), q(o, "class", "svelte-43sxxs"), q(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(_, "fill", "#FF7C00"), q(_, "class", "svelte-43sxxs"), q(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(c, "fill", "#FF7C00"), q(c, "fill-opacity", "0.4"), q(c, "class", "svelte-43sxxs"), q(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(d, "fill", "#FF7C00"), q(d, "class", "svelte-43sxxs"), ue(a, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), He(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(u, h) {
      cn(u, e, h), P(e, t), P(t, l), P(l, i), P(l, f), P(l, s), P(l, r), P(t, a), P(a, o), P(a, _), P(a, c), P(a, d);
    },
    p(u, [h]) {
      h & /*$top*/
      2 && ue(l, "transform", "translate(" + /*$top*/
      u[1][0] + "px, " + /*$top*/
      u[1][1] + "px)"), h & /*$bottom*/
      4 && ue(a, "transform", "translate(" + /*$bottom*/
      u[2][0] + "px, " + /*$bottom*/
      u[2][1] + "px)"), h & /*margin*/
      1 && He(
        e,
        "margin",
        /*margin*/
        u[0]
      );
    },
    i: Re,
    o: Re,
    d(u) {
      u && rn(e);
    }
  };
}
function gn(n, e, t) {
  let l, i, { margin: f = !0 } = e;
  const s = Ge([0, 0]);
  Oe(n, s, (d) => t(1, l = d));
  const r = Ge([0, 0]);
  Oe(n, r, (d) => t(2, i = d));
  let a;
  async function o() {
    await Promise.all([s.set([125, 140]), r.set([-125, -140])]), await Promise.all([s.set([-125, 140]), r.set([125, -140])]), await Promise.all([s.set([-125, 0]), r.set([125, -0])]), await Promise.all([s.set([125, 0]), r.set([-125, 0])]);
  }
  async function _() {
    await o(), a || _();
  }
  async function c() {
    await Promise.all([s.set([125, 0]), r.set([-125, 0])]), _();
  }
  return mn(() => (c(), () => a = !0)), n.$$set = (d) => {
    "margin" in d && t(0, f = d.margin);
  }, [f, l, i, s, r];
}
class hn extends an {
  constructor(e) {
    super(), un(this, e, gn, bn, dn, { margin: 0 });
  }
}
const {
  SvelteComponent: wn,
  append: R,
  attr: Z,
  binding_callbacks: Je,
  check_outros: yt,
  create_component: qt,
  create_slot: kn,
  destroy_component: Ct,
  destroy_each: Ft,
  detach: p,
  element: E,
  empty: le,
  ensure_array_like: he,
  get_all_dirty_from_scope: pn,
  get_slot_changes: vn,
  group_outros: Lt,
  init: yn,
  insert: v,
  mount_component: St,
  noop: Le,
  safe_not_equal: qn,
  set_data: V,
  set_style: Y,
  space: j,
  text: L,
  toggle_class: M,
  transition_in: H,
  transition_out: J,
  update_slot_base: Cn
} = window.__gradio__svelte__internal, { tick: Fn } = window.__gradio__svelte__internal, { onDestroy: Ln } = window.__gradio__svelte__internal, { createEventDispatcher: Sn } = window.__gradio__svelte__internal, zn = (n) => ({}), Ke = (n) => ({});
function Qe(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l[42] = t, l;
}
function Ue(n, e, t) {
  const l = n.slice();
  return l[40] = e[t], l;
}
function Mn(n) {
  let e, t, l, i, f = (
    /*i18n*/
    n[1]("common.error") + ""
  ), s, r, a;
  t = new Ql({
    props: {
      Icon: ln,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const o = (
    /*#slots*/
    n[30].error
  ), _ = kn(
    o,
    n,
    /*$$scope*/
    n[29],
    Ke
  );
  return {
    c() {
      e = E("div"), qt(t.$$.fragment), l = j(), i = E("span"), s = L(f), r = j(), _ && _.c(), Z(e, "class", "clear-status svelte-1yk38uw"), Z(i, "class", "error svelte-1yk38uw");
    },
    m(c, d) {
      v(c, e, d), St(t, e, null), v(c, l, d), v(c, i, d), R(i, s), v(c, r, d), _ && _.m(c, d), a = !0;
    },
    p(c, d) {
      const u = {};
      d[0] & /*i18n*/
      2 && (u.label = /*i18n*/
      c[1]("common.clear")), t.$set(u), (!a || d[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      c[1]("common.error") + "") && V(s, f), _ && _.p && (!a || d[0] & /*$$scope*/
      536870912) && Cn(
        _,
        o,
        c,
        /*$$scope*/
        c[29],
        a ? vn(
          o,
          /*$$scope*/
          c[29],
          d,
          zn
        ) : pn(
          /*$$scope*/
          c[29]
        ),
        Ke
      );
    },
    i(c) {
      a || (H(t.$$.fragment, c), H(_, c), a = !0);
    },
    o(c) {
      J(t.$$.fragment, c), J(_, c), a = !1;
    },
    d(c) {
      c && (p(e), p(l), p(i), p(r)), Ct(t), _ && _.d(c);
    }
  };
}
function Vn(n) {
  let e, t, l, i, f, s, r, a, o, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && We(n)
  );
  function c(m, b) {
    if (
      /*progress*/
      m[7]
    )
      return In;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    )
      return Pn;
    if (
      /*queue_position*/
      m[2] === 0
    )
      return Nn;
  }
  let d = c(n), u = d && d(n), h = (
    /*timer*/
    n[5] && et(n)
  );
  const C = [Dn, Bn], k = [];
  function F(m, b) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = F(n)) && (s = k[f] = C[f](n));
  let g = !/*timer*/
  n[5] && ot(n);
  return {
    c() {
      _ && _.c(), e = j(), t = E("div"), u && u.c(), l = j(), h && h.c(), i = j(), s && s.c(), r = j(), g && g.c(), a = le(), Z(t, "class", "progress-text svelte-1yk38uw"), M(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), M(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(m, b) {
      _ && _.m(m, b), v(m, e, b), v(m, t, b), u && u.m(t, null), R(t, l), h && h.m(t, null), v(m, i, b), ~f && k[f].m(m, b), v(m, r, b), g && g.m(m, b), v(m, a, b), o = !0;
    },
    p(m, b) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? _ ? _.p(m, b) : (_ = We(m), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), d === (d = c(m)) && u ? u.p(m, b) : (u && u.d(1), u = d && d(m), u && (u.c(), u.m(t, l))), /*timer*/
      m[5] ? h ? h.p(m, b) : (h = et(m), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!o || b[0] & /*variant*/
      256) && M(
        t,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!o || b[0] & /*variant*/
      256) && M(
        t,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let B = f;
      f = F(m), f === B ? ~f && k[f].p(m, b) : (s && (Lt(), J(k[B], 1, 1, () => {
        k[B] = null;
      }), yt()), ~f ? (s = k[f], s ? s.p(m, b) : (s = k[f] = C[f](m), s.c()), H(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      m[5] ? g && (g.d(1), g = null) : g ? g.p(m, b) : (g = ot(m), g.c(), g.m(a.parentNode, a));
    },
    i(m) {
      o || (H(s), o = !0);
    },
    o(m) {
      J(s), o = !1;
    },
    d(m) {
      m && (p(e), p(t), p(i), p(r), p(a)), _ && _.d(m), u && u.d(), h && h.d(), ~f && k[f].d(m), g && g.d(m);
    }
  };
}
function We(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = E("div"), Z(e, "class", "eta-bar svelte-1yk38uw"), Y(e, "transform", t);
    },
    m(l, i) {
      v(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && Y(e, "transform", t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Nn(n) {
  let e;
  return {
    c() {
      e = L("processing |");
    },
    m(t, l) {
      v(t, e, l);
    },
    p: Le,
    d(t) {
      t && p(e);
    }
  };
}
function Pn(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, s;
  return {
    c() {
      e = L("queue: "), l = L(t), i = L("/"), f = L(
        /*queue_size*/
        n[3]
      ), s = L(" |");
    },
    m(r, a) {
      v(r, e, a), v(r, l, a), v(r, i, a), v(r, f, a), v(r, s, a);
    },
    p(r, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && V(l, t), a[0] & /*queue_size*/
      8 && V(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (p(e), p(l), p(i), p(f), p(s));
    }
  };
}
function In(n) {
  let e, t = he(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = $e(Ue(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = le();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      v(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = he(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = Ue(i, t, s);
          l[s] ? l[s].p(r, f) : (l[s] = $e(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && p(e), Ft(l, i);
    }
  };
}
function xe(n) {
  let e, t = (
    /*p*/
    n[40].unit + ""
  ), l, i, f = " ", s;
  function r(_, c) {
    return (
      /*p*/
      _[40].length != null ? jn : Zn
    );
  }
  let a = r(n), o = a(n);
  return {
    c() {
      o.c(), e = j(), l = L(t), i = L(" | "), s = L(f);
    },
    m(_, c) {
      o.m(_, c), v(_, e, c), v(_, l, c), v(_, i, c), v(_, s, c);
    },
    p(_, c) {
      a === (a = r(_)) && o ? o.p(_, c) : (o.d(1), o = a(_), o && (o.c(), o.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[40].unit + "") && V(l, t);
    },
    d(_) {
      _ && (p(e), p(l), p(i), p(s)), o.d(_);
    }
  };
}
function Zn(n) {
  let e = $(
    /*p*/
    n[40].index || 0
  ) + "", t;
  return {
    c() {
      t = L(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = $(
        /*p*/
        l[40].index || 0
      ) + "") && V(t, e);
    },
    d(l) {
      l && p(t);
    }
  };
}
function jn(n) {
  let e = $(
    /*p*/
    n[40].index || 0
  ) + "", t, l, i = $(
    /*p*/
    n[40].length
  ) + "", f;
  return {
    c() {
      t = L(e), l = L("/"), f = L(i);
    },
    m(s, r) {
      v(s, t, r), v(s, l, r), v(s, f, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = $(
        /*p*/
        s[40].index || 0
      ) + "") && V(t, e), r[0] & /*progress*/
      128 && i !== (i = $(
        /*p*/
        s[40].length
      ) + "") && V(f, i);
    },
    d(s) {
      s && (p(t), p(l), p(f));
    }
  };
}
function $e(n) {
  let e, t = (
    /*p*/
    n[40].index != null && xe(n)
  );
  return {
    c() {
      t && t.c(), e = le();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].index != null ? t ? t.p(l, i) : (t = xe(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && p(e), t && t.d(l);
    }
  };
}
function et(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = L(
        /*formatted_timer*/
        n[20]
      ), l = L(t), i = L("s");
    },
    m(f, s) {
      v(f, e, s), v(f, l, s), v(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && V(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && V(l, t);
    },
    d(f) {
      f && (p(e), p(l), p(i));
    }
  };
}
function Bn(n) {
  let e, t;
  return e = new hn({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      qt(e.$$.fragment);
    },
    m(l, i) {
      St(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (H(e.$$.fragment, l), t = !0);
    },
    o(l) {
      J(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ct(e, l);
    }
  };
}
function Dn(n) {
  let e, t, l, i, f, s = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && tt(n)
  );
  return {
    c() {
      e = E("div"), t = E("div"), r && r.c(), l = j(), i = E("div"), f = E("div"), Z(t, "class", "progress-level-inner svelte-1yk38uw"), Z(f, "class", "progress-bar svelte-1yk38uw"), Y(f, "width", s), Z(i, "class", "progress-bar-wrap svelte-1yk38uw"), Z(e, "class", "progress-level svelte-1yk38uw");
    },
    m(a, o) {
      v(a, e, o), R(e, t), r && r.m(t, null), R(e, l), R(e, i), R(i, f), n[31](f);
    },
    p(a, o) {
      /*progress*/
      a[7] != null ? r ? r.p(a, o) : (r = tt(a), r.c(), r.m(t, null)) : r && (r.d(1), r = null), o[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      a[15] * 100}%`) && Y(f, "width", s);
    },
    i: Le,
    o: Le,
    d(a) {
      a && p(e), r && r.d(), n[31](null);
    }
  };
}
function tt(n) {
  let e, t = he(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = st(Qe(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = le();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      v(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = he(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = Qe(i, t, s);
          l[s] ? l[s].p(r, f) : (l[s] = st(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && p(e), Ft(l, i);
    }
  };
}
function lt(n) {
  let e, t, l, i, f = (
    /*i*/
    n[42] !== 0 && An()
  ), s = (
    /*p*/
    n[40].desc != null && nt(n)
  ), r = (
    /*p*/
    n[40].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null && it()
  ), a = (
    /*progress_level*/
    n[14] != null && ft(n)
  );
  return {
    c() {
      f && f.c(), e = j(), s && s.c(), t = j(), r && r.c(), l = j(), a && a.c(), i = le();
    },
    m(o, _) {
      f && f.m(o, _), v(o, e, _), s && s.m(o, _), v(o, t, _), r && r.m(o, _), v(o, l, _), a && a.m(o, _), v(o, i, _);
    },
    p(o, _) {
      /*p*/
      o[40].desc != null ? s ? s.p(o, _) : (s = nt(o), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      o[40].desc != null && /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[42]
      ] != null ? r || (r = it(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      o[14] != null ? a ? a.p(o, _) : (a = ft(o), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(o) {
      o && (p(e), p(t), p(l), p(i)), f && f.d(o), s && s.d(o), r && r.d(o), a && a.d(o);
    }
  };
}
function An(n) {
  let e;
  return {
    c() {
      e = L(" /");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && p(e);
    }
  };
}
function nt(n) {
  let e = (
    /*p*/
    n[40].desc + ""
  ), t;
  return {
    c() {
      t = L(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[40].desc + "") && V(t, e);
    },
    d(l) {
      l && p(t);
    }
  };
}
function it(n) {
  let e;
  return {
    c() {
      e = L("-");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && p(e);
    }
  };
}
function ft(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[42]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = L(e), l = L("%");
    },
    m(i, f) {
      v(i, t, f), v(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[42]
      ] || 0)).toFixed(1) + "") && V(t, e);
    },
    d(i) {
      i && (p(t), p(l));
    }
  };
}
function st(n) {
  let e, t = (
    /*p*/
    (n[40].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[42]
    ] != null) && lt(n)
  );
  return {
    c() {
      t && t.c(), e = le();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[40].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[42]
      ] != null ? t ? t.p(l, i) : (t = lt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && p(e), t && t.d(l);
    }
  };
}
function ot(n) {
  let e, t;
  return {
    c() {
      e = E("p"), t = L(
        /*loading_text*/
        n[9]
      ), Z(e, "class", "loading svelte-1yk38uw");
    },
    m(l, i) {
      v(l, e, i), R(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && V(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && p(e);
    }
  };
}
function En(n) {
  let e, t, l, i, f;
  const s = [Vn, Mn], r = [];
  function a(o, _) {
    return (
      /*status*/
      o[4] === "pending" ? 0 : (
        /*status*/
        o[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(n)) && (l = r[t] = s[t](n)), {
    c() {
      e = E("div"), l && l.c(), Z(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1yk38uw"), M(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), M(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), M(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), M(
        e,
        "border",
        /*border*/
        n[12]
      ), Y(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Y(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(o, _) {
      v(o, e, _), ~t && r[t].m(e, null), n[33](e), f = !0;
    },
    p(o, _) {
      let c = t;
      t = a(o), t === c ? ~t && r[t].p(o, _) : (l && (Lt(), J(r[c], 1, 1, () => {
        r[c] = null;
      }), yt()), ~t ? (l = r[t], l ? l.p(o, _) : (l = r[t] = s[t](o), l.c()), H(l, 1), l.m(e, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      o[8] + " " + /*show_progress*/
      o[6] + " svelte-1yk38uw")) && Z(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && M(e, "hide", !/*status*/
      o[4] || /*status*/
      o[4] === "complete" || /*show_progress*/
      o[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && M(
        e,
        "translucent",
        /*variant*/
        o[8] === "center" && /*status*/
        (o[4] === "pending" || /*status*/
        o[4] === "error") || /*translucent*/
        o[11] || /*show_progress*/
        o[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && M(
        e,
        "generating",
        /*status*/
        o[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && M(
        e,
        "border",
        /*border*/
        o[12]
      ), _[0] & /*absolute*/
      1024 && Y(
        e,
        "position",
        /*absolute*/
        o[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Y(
        e,
        "padding",
        /*absolute*/
        o[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(o) {
      f || (H(l), f = !0);
    },
    o(o) {
      J(l), f = !1;
    },
    d(o) {
      o && p(e), ~t && r[t].d(), n[33](null);
    }
  };
}
let ce = [], ye = !1;
async function Tn(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (ce.push(n), !ye)
      ye = !0;
    else
      return;
    await Fn(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < ce.length; l++) {
        const f = ce[l].getBoundingClientRect();
        (l === 0 || f.top + window.scrollY <= t[0]) && (t[0] = f.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), ye = !1, ce = [];
    });
  }
}
function Xn(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e;
  const s = Sn();
  let { i18n: r } = e, { eta: a = null } = e, { queue_position: o } = e, { queue_size: _ } = e, { status: c } = e, { scroll_to_output: d = !1 } = e, { timer: u = !0 } = e, { show_progress: h = "full" } = e, { message: C = null } = e, { progress: k = null } = e, { variant: F = "default" } = e, { loading_text: g = "Loading..." } = e, { absolute: m = !0 } = e, { translucent: b = !1 } = e, { border: B = !1 } = e, { autoscroll: y } = e, ne, ie = !1, ae = 0, G = 0, K = null, Q = null, Pe = 0, O = null, fe, X = null, Ie = !0;
  const Nt = () => {
    t(0, a = t(27, K = t(19, re = null))), t(25, ae = performance.now()), t(26, G = 0), ie = !0, Ze();
  };
  function Ze() {
    requestAnimationFrame(() => {
      t(26, G = (performance.now() - ae) / 1e3), ie && Ze();
    });
  }
  function je() {
    t(26, G = 0), t(0, a = t(27, K = t(19, re = null))), ie && (ie = !1);
  }
  Ln(() => {
    ie && je();
  });
  let re = null;
  function Pt(w) {
    Je[w ? "unshift" : "push"](() => {
      X = w, t(16, X), t(7, k), t(14, O), t(15, fe);
    });
  }
  const It = () => {
    s("clear_status");
  };
  function Zt(w) {
    Je[w ? "unshift" : "push"](() => {
      ne = w, t(13, ne);
    });
  }
  return n.$$set = (w) => {
    "i18n" in w && t(1, r = w.i18n), "eta" in w && t(0, a = w.eta), "queue_position" in w && t(2, o = w.queue_position), "queue_size" in w && t(3, _ = w.queue_size), "status" in w && t(4, c = w.status), "scroll_to_output" in w && t(22, d = w.scroll_to_output), "timer" in w && t(5, u = w.timer), "show_progress" in w && t(6, h = w.show_progress), "message" in w && t(23, C = w.message), "progress" in w && t(7, k = w.progress), "variant" in w && t(8, F = w.variant), "loading_text" in w && t(9, g = w.loading_text), "absolute" in w && t(10, m = w.absolute), "translucent" in w && t(11, b = w.translucent), "border" in w && t(12, B = w.border), "autoscroll" in w && t(24, y = w.autoscroll), "$$scope" in w && t(29, f = w.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = K), a != null && K !== a && (t(28, Q = (performance.now() - ae) / 1e3 + a), t(19, re = Q.toFixed(1)), t(27, K = a))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, Pe = Q === null || Q <= 0 || !G ? null : Math.min(G / Q, 1)), n.$$.dirty[0] & /*progress*/
    128 && k != null && t(18, Ie = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (k != null ? t(14, O = k.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, O = null), O ? (t(15, fe = O[O.length - 1]), X && (fe === 0 ? t(16, X.style.transition = "0", X) : t(16, X.style.transition = "150ms", X))) : t(15, fe = void 0)), n.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? Nt() : je()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && ne && d && (c === "pending" || c === "complete") && Tn(ne, y), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = G.toFixed(1));
  }, [
    a,
    r,
    o,
    _,
    c,
    u,
    h,
    k,
    F,
    g,
    m,
    b,
    B,
    ne,
    O,
    fe,
    X,
    Pe,
    Ie,
    re,
    l,
    s,
    d,
    C,
    y,
    ae,
    G,
    K,
    Q,
    f,
    i,
    Pt,
    It,
    Zt
  ];
}
class Yn extends wn {
  constructor(e) {
    super(), yn(
      this,
      e,
      Xn,
      En,
      qn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Gn,
  add_render_callback: On,
  append: Se,
  assign: Rn,
  attr: Hn,
  check_outros: Jn,
  create_component: Me,
  destroy_component: Ve,
  destroy_each: Kn,
  detach: we,
  element: ze,
  ensure_array_like: at,
  get_spread_object: Qn,
  get_spread_update: Un,
  group_outros: Wn,
  init: xn,
  insert: ke,
  listen: $n,
  mount_component: Ne,
  safe_not_equal: ei,
  select_option: rt,
  select_value: ti,
  set_data: zt,
  set_input_value: _t,
  space: ut,
  text: Mt,
  toggle_class: li,
  transition_in: ee,
  transition_out: oe
} = window.__gradio__svelte__internal;
function ct(n, e, t) {
  const l = n.slice();
  return l[17] = e[t], l;
}
function dt(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[9].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[9].i18n
    ) },
    /*loading_status*/
    n[8]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = Rn(i, l[f]);
  return e = new Yn({ props: i }), {
    c() {
      Me(e.$$.fragment);
    },
    m(f, s) {
      Ne(e, f, s), t = !0;
    },
    p(f, s) {
      const r = s & /*gradio, loading_status*/
      768 ? Un(l, [
        s & /*gradio*/
        512 && { autoscroll: (
          /*gradio*/
          f[9].autoscroll
        ) },
        s & /*gradio*/
        512 && { i18n: (
          /*gradio*/
          f[9].i18n
        ) },
        s & /*loading_status*/
        256 && Qn(
          /*loading_status*/
          f[8]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (ee(e.$$.fragment, f), t = !0);
    },
    o(f) {
      oe(e.$$.fragment, f), t = !1;
    },
    d(f) {
      Ve(e, f);
    }
  };
}
function ni(n) {
  let e;
  return {
    c() {
      e = Mt(
        /*label*/
        n[0]
      );
    },
    m(t, l) {
      ke(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      1 && zt(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && we(e);
    }
  };
}
function mt(n) {
  let e, t = (
    /*choice*/
    n[17][0] + ""
  ), l, i;
  return {
    c() {
      e = ze("option"), l = Mt(t), e.__value = i = /*choice*/
      n[17][0], _t(e, e.__value);
    },
    m(f, s) {
      ke(f, e, s), Se(e, l);
    },
    p(f, s) {
      s & /*choices*/
      16 && t !== (t = /*choice*/
      f[17][0] + "") && zt(l, t), s & /*choices*/
      16 && i !== (i = /*choice*/
      f[17][0]) && (e.__value = i, _t(e, e.__value));
    },
    d(f) {
      f && we(e);
    }
  };
}
function ii(n) {
  let e, t, l, i, f, s, r, a, o, _ = (
    /*loading_status*/
    n[8] && dt(n)
  );
  l = new Il({
    props: {
      show_label: (
        /*show_label*/
        n[5]
      ),
      info: void 0,
      $$slots: { default: [ni] },
      $$scope: { ctx: n }
    }
  });
  let c = at(
    /*choices*/
    n[4]
  ), d = [];
  for (let u = 0; u < c.length; u += 1)
    d[u] = mt(ct(n, c, u));
  return {
    c() {
      _ && _.c(), e = ut(), t = ze("label"), Me(l.$$.fragment), i = ut(), f = ze("select");
      for (let u = 0; u < d.length; u += 1)
        d[u].c();
      f.disabled = s = !/*interactive*/
      n[10], Hn(f, "class", "svelte-nd0hqn"), /*display_value*/
      n[11] === void 0 && On(() => (
        /*select_change_handler*/
        n[15].call(f)
      )), li(t, "container", Vt);
    },
    m(u, h) {
      _ && _.m(u, h), ke(u, e, h), ke(u, t, h), Ne(l, t, null), Se(t, i), Se(t, f);
      for (let C = 0; C < d.length; C += 1)
        d[C] && d[C].m(f, null);
      rt(
        f,
        /*display_value*/
        n[11],
        !0
      ), r = !0, a || (o = $n(
        f,
        "change",
        /*select_change_handler*/
        n[15]
      ), a = !0);
    },
    p(u, h) {
      /*loading_status*/
      u[8] ? _ ? (_.p(u, h), h & /*loading_status*/
      256 && ee(_, 1)) : (_ = dt(u), _.c(), ee(_, 1), _.m(e.parentNode, e)) : _ && (Wn(), oe(_, 1, 1, () => {
        _ = null;
      }), Jn());
      const C = {};
      if (h & /*show_label*/
      32 && (C.show_label = /*show_label*/
      u[5]), h & /*$$scope, label*/
      1048577 && (C.$$scope = { dirty: h, ctx: u }), l.$set(C), h & /*choices*/
      16) {
        c = at(
          /*choices*/
          u[4]
        );
        let k;
        for (k = 0; k < c.length; k += 1) {
          const F = ct(u, c, k);
          d[k] ? d[k].p(F, h) : (d[k] = mt(F), d[k].c(), d[k].m(f, null));
        }
        for (; k < d.length; k += 1)
          d[k].d(1);
        d.length = c.length;
      }
      (!r || h & /*interactive*/
      1024 && s !== (s = !/*interactive*/
      u[10])) && (f.disabled = s), h & /*display_value, choices*/
      2064 && rt(
        f,
        /*display_value*/
        u[11]
      );
    },
    i(u) {
      r || (ee(_), ee(l.$$.fragment, u), r = !0);
    },
    o(u) {
      oe(_), oe(l.$$.fragment, u), r = !1;
    },
    d(u) {
      u && (we(e), we(t)), _ && _.d(u), Ve(l), Kn(d, u), a = !1, o();
    }
  };
}
function fi(n) {
  let e, t;
  return e = new Ut({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      padding: Vt,
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[6]
      ),
      min_width: (
        /*min_width*/
        n[7]
      ),
      $$slots: { default: [ii] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Me(e.$$.fragment);
    },
    m(l, i) {
      Ne(e, l, i), t = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      8 && (f.visible = /*visible*/
      l[3]), i & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      l[2]), i & /*scale*/
      64 && (f.scale = /*scale*/
      l[6]), i & /*min_width*/
      128 && (f.min_width = /*min_width*/
      l[7]), i & /*$$scope, interactive, display_value, choices, show_label, label, gradio, loading_status*/
      1052465 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (ee(e.$$.fragment, l), t = !0);
    },
    o(l) {
      oe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ve(e, l);
    }
  };
}
const Vt = !0;
function si(n, e, t) {
  let { label: l = "Dropdown" } = e, { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: s = !0 } = e, { value: r } = e, { value_is_output: a = !1 } = e, { choices: o } = e, { show_label: _ } = e, { scale: c = null } = e, { min_width: d = void 0 } = e, { loading_status: u } = e, { gradio: h } = e, { interactive: C } = e, k, F;
  function g() {
    h.dispatch("change"), a || h.dispatch("input");
  }
  function m() {
    k = ti(this), t(11, k), t(4, o);
  }
  return n.$$set = (b) => {
    "label" in b && t(0, l = b.label), "elem_id" in b && t(1, i = b.elem_id), "elem_classes" in b && t(2, f = b.elem_classes), "visible" in b && t(3, s = b.visible), "value" in b && t(12, r = b.value), "value_is_output" in b && t(13, a = b.value_is_output), "choices" in b && t(4, o = b.choices), "show_label" in b && t(5, _ = b.show_label), "scale" in b && t(6, c = b.scale), "min_width" in b && t(7, d = b.min_width), "loading_status" in b && t(8, u = b.loading_status), "gradio" in b && t(9, h = b.gradio), "interactive" in b && t(10, C = b.interactive);
  }, n.$$.update = () => {
    n.$$.dirty & /*display_value, choices, candidate*/
    18448 && k && (t(14, F = o.filter((b) => b[0] === k)), t(12, r = F.length ? F[0][1] : "")), n.$$.dirty & /*value*/
    4096 && g();
  }, [
    l,
    i,
    f,
    s,
    o,
    _,
    c,
    d,
    u,
    h,
    C,
    k,
    r,
    a,
    F,
    m
  ];
}
class oi extends Gn {
  constructor(e) {
    super(), xn(this, e, si, fi, ei, {
      label: 0,
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 12,
      value_is_output: 13,
      choices: 4,
      show_label: 5,
      scale: 6,
      min_width: 7,
      loading_status: 8,
      gradio: 9,
      interactive: 10
    });
  }
}
export {
  oi as default
};
