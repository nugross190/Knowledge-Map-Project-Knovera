/* Swipe feed ("Mode geser"), shared by the map, bank and TKA pages (templates/_feed.js; styles: _feed.css).
   makeFeed(dialog, handlers) drives a <dialog class="feed"> that holds a close button (.st-close) and a scroller
   (.st-feed) whose children are equal-height slides snapping one per screen. The page fills the slides and handles
   taps inside them. The feed opens the dialog as a modal (the page behind is inert; Esc or the Android back gesture
   closes it), keeps ?mode=geser in the address while open, tracks the slide on screen, and moves between slides with
   the arrow and Page keys; an arrow key scrolls a long card (.st-body) to its end before moving on.
   handlers: onClose(slide) runs after closing, with the slide that was on screen; onSide(dir) gets ← (-1) and → (1);
   onNearEnd() runs when the reader is within three slides of the end, so the page can add more. */
function makeFeed(dialog, handlers = {}){
  const scroller = dialog.querySelector(".st-feed");
  const motion = () => matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
  const clamp = i => Math.max(0, Math.min(scroller.children.length - 1, i));
  // Every slide is exactly one scroller tall (_feed.css), so the slide on screen follows from the scroll position.
  const onScreen = () => clamp(Math.round(scroller.scrollTop / (scroller.clientHeight || 1)));
  // While the feed scrolls by itself (a key, a button, a graded card), the next key counts from where that scroll is
  // going, not from a half-way position, so quick presses add up. The goals end when the scrolling settles (no scroll
  // event for 150 ms) or as soon as the reader takes over with a swipe, the wheel or another key.
  let goal = null, settling = 0, lastSlide = null;
  const cardGoal = new Map();  // card body → the scrollTop it is heading to
  const at = () => goal === null ? onScreen() : goal;
  function forget(){ clearTimeout(settling); goal = null; cardGoal.clear(); }
  function settleLater(){ clearTimeout(settling); settling = setTimeout(forget, 150); }
  function go(i, animate){
    if(!scroller.children.length) return;
    goal = clamp(i);
    scroller.scrollTo({top: scroller.children[goal].offsetTop, behavior: animate ? motion() : "auto"});
    settleLater();
  }
  function scrollCard(body, dir){
    const end = body.scrollHeight - body.clientHeight;
    const from = cardGoal.has(body) ? cardGoal.get(body) : body.scrollTop;
    if(dir > 0 ? from >= end - 1 : from <= 0) return false;
    const to = Math.max(0, Math.min(end, from + dir * body.clientHeight * 0.8));
    cardGoal.set(body, to);
    body.scrollTo({top: to, behavior: motion()});
    settleLater();
    return true;
  }
  function setMode(on){
    const url = new URL(location.href);
    on ? url.searchParams.set("mode", "geser") : url.searchParams.delete("mode");
    try { history.replaceState(history.state, "", url); } catch(e) {}
  }
  const feed = {
    scroller,
    get isOpen(){ return dialog.open; },
    current: () => scroller.children[at()] || null,
    go: i => go(i, true),
    move: dir => go(at() + dir, true),
    open(html, start){
      scroller.innerHTML = html;
      if(!dialog.open) dialog.showModal ? dialog.showModal() : dialog.setAttribute("open", "");
      document.body.classList.add("feed-open");
      go(start || 0, false);
      scroller.focus({preventScroll: true});  // not the close button, so Space never closes the feed
      setMode(true);
    },
    close(){
      if(!dialog.open) return;
      lastSlide = feed.current();
      if(dialog.close) dialog.close();
      else { dialog.removeAttribute("open"); dialog.dispatchEvent(new Event("close")); }
    },
  };
  // The slide on screen is read before the dialog hides (a hidden scroller reports scrollTop 0): in close(), or in the
  // cancel event that Esc and the Android back gesture fire first.
  dialog.addEventListener("cancel", () => { lastSlide = feed.current(); });
  dialog.addEventListener("close", () => {
    const slide = lastSlide;
    lastSlide = null;
    forget();
    document.body.classList.remove("feed-open");
    setMode(false);
    if(handlers.onClose) handlers.onClose(slide);
  });
  dialog.querySelector(".st-close").addEventListener("click", feed.close);
  dialog.addEventListener("pointerdown", forget);
  dialog.addEventListener("wheel", forget, {passive: true});
  // Capturing, so it also hears the cards: scroll events do not bubble, but they do pass through the capture phase.
  scroller.addEventListener("scroll", e => {
    if(goal !== null || cardGoal.size) settleLater();
    if(e.target === scroller && handlers.onNearEnd && scroller.scrollTop + scroller.clientHeight * 3 >= scroller.scrollHeight) handlers.onNearEnd();
  }, {capture: true, passive: true});
  // On the document, not the dialog: when a focused button is disabled (after an answer is checked), focus falls
  // back to <body>, outside the dialog, and the keys must still work.
  document.addEventListener("keydown", e => {
    if(!dialog.open || e.defaultPrevented) return;
    const dir = {ArrowDown: 1, PageDown: 1, ArrowUp: -1, PageUp: -1}[e.key];
    const side = {ArrowLeft: -1, ArrowRight: 1}[e.key];
    if(e.altKey || e.ctrlKey || e.metaKey || e.target.closest("input, select, textarea") || !(dir || (side && handlers.onSide))){
      forget();  // the reader's own key (Space, Home, a radio button's arrows): whatever it scrolls is theirs
      return;
    }
    e.preventDefault();
    if(side) return handlers.onSide(side);
    const body = feed.current() && feed.current().querySelector(".st-body");
    if(!(e.key.startsWith("Arrow") && body && scrollCard(body, dir))) feed.move(dir);
  });
  return feed;
}
