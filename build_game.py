# -*- coding: utf-8 -*-
"""
Toplama ve Çıkarma Dedektifleri - Complete Interactive HTML Game Generator
Generates index.html with all resim/ assets, cropped buttons, Web Audio API,
audio narration queue, all 10 pedagogical questions, and self-evaluation certificate.
"""

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover" />
  <title>Toplama ve Çıkarma Dedektifleri</title>
  <style>
    @font-face {
      font-family: 'TTKBDikTemel';
      src: url('./TTKBDikTemelAbeceBody.ttf') format('truetype');
      font-weight: normal;
      font-style: normal;
      font-display: swap;
    }

    :root {
      --font-main: 'TTKBDikTemel', 'Comic Sans MS', 'Fredoka', 'Nunito', system-ui, -apple-system, sans-serif;
      --navy-900: #0a1128;
      --navy-800: #0f1c3f;
      --blue-600: #2563eb;
      --blue-500: #3b82f6;
      --yellow-400: #facc15;
      --yellow-500: #eab308;
      --gold-dark: #854d0e;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      width: 100%;
      height: 100%;
      background: #091222;
      font-family: var(--font-main);
      color: #1e293b;
      overflow: hidden;
      user-select: none;
    }

    /* Outer Viewport: centers the 16:9 game stage */
    .game-viewport {
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at center, #132440 0%, #080f1d 100%);
      padding: clamp(4px, 1.2vw, 16px);
      position: relative;
    }

    /* Confetti Canvas for Celebrations */
    #confetti-canvas {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 999;
      width: 100%;
      height: 100%;
    }

    /* 16:9 Master Container */
    .game-stage {
      position: relative;
      width: 100%;
      max-width: 1440px;
      aspect-ratio: 16 / 9;
      max-height: 98vh;
      background: #000;
      border-radius: clamp(14px, 2vw, 26px);
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 0 3px rgba(255, 255, 255, 0.12);
    }

    /* Screen Elements */
    .screen {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: none;
      background-size: 100% 100%;
      background-position: center;
      background-repeat: no-repeat;
    }

    .screen.active {
      display: block;
      animation: screenFadeIn 0.28s ease-out;
    }

    @keyframes screenFadeIn {
      from { opacity: 0; transform: scale(0.99); }
      to { opacity: 1; transform: scale(1); }
    }

    /* Backgrounds from user assets */
    #screen-cover {
      background-image: url('resim/dedektif ai-02.png');
    }

    #screen-intro {
      background-image: url('resim/dedektif ai-04.png');
    }

    #screen-map {
      background-image: url('resim/dedektif ai-03.png');
    }

    #screen-question.char-boy {
      background-image: url('resim/dedektif ai-08.png');
    }

    #screen-question.char-girl {
      background-image: url('resim/dedektif ai-10.png');
    }

    #screen-question.char-girl .question-box-parchment {
      left: 21%;
      top: 19.5%;
      width: 63.5%;
      height: 28%;
    }

    #screen-question.char-girl .options-row-container {
      top: 51.5%;
    }

    #screen-question.char-girl .detective-hint-banner {
      top: 70%;
    }

    #screen-correct,
    #screen-eval {
      background-image: url('resim/dedektif ai-11.png');
    }

    #screen-wrong {
      background-image: url('resim/dedektif ai-09.png');
    }

    /* Image Buttons */
    .img-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      cursor: pointer;
      padding: 0;
      user-select: none;
      transition: transform 0.16s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.16s ease;
      touch-action: manipulation;
    }

    .img-btn img {
      display: block;
      width: auto;
      height: 100%;
      max-height: 100%;
      object-fit: contain;
      pointer-events: none;
    }

    .img-btn:hover {
      transform: translateY(-3px) scale(1.05);
      filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.45));
    }

    .img-btn:active {
      transform: translateY(1px) scale(0.96);
    }

    /* Top HUD / Controls */
    .hud-header {
      position: absolute;
      top: 2%;
      left: 2%;
      right: 2%;
      height: 9%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 30;
      pointer-events: none;
    }

    .hud-left, .hud-right {
      display: flex;
      align-items: center;
      gap: clamp(6px, 1vw, 14px);
      pointer-events: auto;
    }

    /* Section / Station Info Badge */
    .station-pill-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(10, 25, 59, 0.88);
      border: 2px solid #60a5fa;
      border-radius: 9999px;
      padding: 6px 16px;
      color: #ffffff;
      font-weight: bold;
      font-size: clamp(0.9rem, 1.3vw, 1.25rem);
      box-shadow: 0 4px 14px rgba(0,0,0,0.3);
      backdrop-filter: blur(6px);
    }

    .station-pill-badge .star-icon {
      color: #facc15;
    }

    /* Round Icon Buttons (Sound, Fullscreen, Replay) */
    .icon-round-btn {
      width: clamp(38px, 3.8vw, 52px);
      height: clamp(38px, 3.8vw, 52px);
      border-radius: 50%;
      background: rgba(13, 27, 62, 0.9);
      border: 2px solid #93c5fd;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
      transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
      touch-action: manipulation;
    }

    .icon-round-btn svg {
      width: 58%;
      height: 58%;
    }

    .icon-round-btn:hover {
      transform: scale(1.08);
      background: #1d4ed8;
      border-color: #facc15;
    }

    .icon-round-btn:active {
      transform: scale(0.94);
    }

    .icon-round-btn.pulse-active {
      animation: audioPulse 1.4s infinite;
      border-color: #facc15;
      background: #2563eb;
    }

    @keyframes audioPulse {
      0% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.7); }
      70% { box-shadow: 0 0 0 14px rgba(250, 204, 21, 0); }
      100% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0); }
    }

    /* Small Nav Buttons using Images */
    .hud-btn-img {
      height: clamp(36px, 3.8vw, 50px);
    }

    /* ========================================================
       SCREEN: COVER
       ======================================================== */
    /* Interactive Hotspot directly over the pre-drawn "Maceraya Başla" button */
    .cover-start-hotspot {
      position: absolute;
      left: 40.5%;
      top: 88.4%;
      width: 17.4%;
      height: 9.9%;
      border-radius: 9999px;
      cursor: pointer;
      z-index: 25;
      border: 3px solid transparent;
      box-sizing: border-box;
      transition: border-color 0.18s ease, box-shadow 0.18s ease;
      touch-action: manipulation;
    }

    .cover-start-hotspot:hover {
      border-color: #facc15;
      box-shadow: 0 0 16px 2px rgba(250, 204, 21, 0.75), inset 0 0 10px rgba(255, 255, 255, 0.35);
    }

    .cover-start-hotspot:active {
      transform: scale(0.985);
    }

    /* ========================================================
       SCREEN: INTRO / NASIL OYNANIR?
       ======================================================== */
    .intro-bottom-btn {
      position: absolute;
      left: 66.5%;
      top: 61.3%;
      width: 20%;
      height: 11.5%;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 20;
    }

    /* ========================================================
       SCREEN: GAME MAP
       ======================================================== */
    .map-hotspots-container {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
    }

    /* 5 Station Interactive Cards matching EXACT card perimeters on resim/dedektif ai-03.png */
    .station-card-hotspot {
      position: absolute;
      cursor: pointer;
      border: 3.5px solid transparent;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      align-items: center;
      padding: 8px;
      box-sizing: border-box;
      touch-action: manipulation;
    }

    .station-card-hotspot:hover {
      border-color: #facc15;
      box-shadow: 0 0 20px 4px rgba(250, 204, 21, 0.8), inset 0 0 14px rgba(255, 255, 255, 0.35);
    }

    /* Exact Pixel-Perfect Coordinates measured from 4000x2250 graphic */
    .station-spot-1 { left: 12.5%; top: 24.8%; width: 23.1%; height: 26.1%; border-radius: clamp(14px, 2vw, 28px); }
    .station-spot-2 { left: 38.8%; top: 24.8%; width: 23.1%; height: 26.1%; border-radius: clamp(14px, 2vw, 28px); }
    .station-spot-3 { left: 65.1%; top: 24.8%; width: 23.1%; height: 26.1%; border-radius: clamp(14px, 2vw, 28px); }
    .station-spot-4 { left: 24.5%; top: 55.1%; width: 25.0%; height: 28.4%; border-radius: clamp(16px, 2.2vw, 32px); }
    .station-spot-5 { left: 55.8%; top: 55.1%; width: 25.0%; height: 28.4%; border-radius: clamp(16px, 2.2vw, 32px); }

    /* Completion Stars / Status Badge on Map */
    .map-station-badge {
      background: linear-gradient(180deg, #16a34a 0%, #14532d 100%);
      color: #ffffff;
      border: 2px solid #86efac;
      border-radius: 9999px;
      padding: 4px 14px;
      font-size: clamp(0.8rem, 1.1vw, 1.05rem);
      font-weight: bold;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      margin-bottom: 4px;
      animation: badgePop 0.3s ease;
    }

    @keyframes badgePop {
      0% { transform: scale(0.6); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }

    /* ========================================================
       SCREEN: QUESTION (Matches resim/dedektif ai-05.png)
       ======================================================== */
    /* Dashed Question Box */
    .question-box-parchment {
      position: absolute;
      left: 20.5%;
      top: 11.2%;
      width: 63.5%;
      height: 27.5%;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 15;
    }

    .q-dashed-card {
      width: 100%;
      height: 100%;
      background-image: url('resim/frame_question_banner.png');
      background-size: 100% 100%;
      background-repeat: no-repeat;
      background-position: center;
      background-color: transparent;
      border: none;
      border-radius: 0;
      box-shadow: none;
      backdrop-filter: none;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: clamp(8px, 1.2vw, 16px) clamp(24px, 3.5vw, 56px);
      position: relative;
      cursor: pointer;
      box-sizing: border-box;
      filter: drop-shadow(0 4px 12px rgba(100, 50, 10, 0.18));
      transition: filter 0.16s ease, transform 0.14s ease;
    }

    .q-dashed-card:hover {
      filter: drop-shadow(0 6px 18px rgba(100, 50, 10, 0.28));
      transform: scale(1.008);
    }

    .q-text-content {
      font-family: var(--font-main);
      font-size: clamp(1.2rem, 2.05vw, 2.05rem);
      font-weight: 800;
      color: #0c1844;
      line-height: 1.34;
      text-align: center;
      max-width: 94%;
    }

    .q-math-expr {
      font-size: 1.18em;
      font-weight: 900;
      color: #0c1844;
      margin-bottom: 2px;
    }

    .q-speaker-mini {
      position: absolute;
      right: 12px;
      top: 12px;
      width: clamp(34px, 3.2vw, 44px);
      height: clamp(34px, 3.2vw, 44px);
      border-radius: 50%;
      background: #2563eb;
      color: #ffffff;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 10px rgba(37,99,235,0.4);
      transition: transform 0.14s ease, background 0.14s ease;
    }

    .q-speaker-mini:hover {
      transform: scale(1.1);
      background: #1d4ed8;
    }

    .q-speaker-mini svg {
      width: 55%;
      height: 55%;
    }

    /* 3 Option Pill Buttons (Matching resim/dedektif ai-05.png) */
    .options-row-container {
      position: absolute;
      left: 20.5%;
      top: 42.5%;
      width: 63.5%;
      display: flex;
      gap: clamp(10px, 1.5vw, 20px);
      justify-content: space-between;
      z-index: 15;
    }

    .opt-pill-btn {
      flex: 1;
      display: flex;
      align-items: center;
      gap: clamp(8px, 1vw, 14px);
      padding: clamp(8px, 1vw, 14px) clamp(12px, 1.5vw, 20px);
      border-radius: 9999px;
      background: linear-gradient(180deg, #1d4ed8 0%, #0d1e56 100%);
      border: 3px solid #60a5fa;
      color: #ffffff;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(13, 30, 86, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.25);
      transition: transform 0.16s cubic-bezier(0.34, 1.56, 0.64, 1), border-color 0.16s ease, box-shadow 0.16s ease;
      touch-action: manipulation;
    }

    .opt-pill-btn:hover {
      transform: translateY(-3px) scale(1.035);
      border-color: #facc15;
      box-shadow: 0 12px 28px rgba(13, 30, 86, 0.6), inset 0 2px 6px rgba(250, 204, 21, 0.35);
    }

    .opt-pill-btn:active {
      transform: translateY(1px) scale(0.97);
    }

    .opt-pill-btn.reading-active {
      border-color: #facc15;
      background: linear-gradient(180deg, #2563eb 0%, #1e40af 100%);
      box-shadow: 0 0 22px rgba(250, 204, 21, 0.85);
      transform: scale(1.05);
    }

    .opt-letter-circle {
      width: clamp(34px, 3.4vw, 46px);
      height: clamp(34px, 3.4vw, 46px);
      min-width: clamp(34px, 3.4vw, 46px);
      border-radius: 50%;
      background: #ffffff;
      color: #0c1844;
      font-family: var(--font-main);
      font-weight: 900;
      font-size: clamp(1.1rem, 1.6vw, 1.5rem);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid #0c1844;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    .opt-text-label {
      font-family: var(--font-main);
      font-weight: bold;
      font-size: clamp(1.05rem, 1.65vw, 1.55rem);
      color: #ffffff;
      line-height: 1.25;
      text-align: left;
      text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    /* Detective Hint Banner (Bottom of Question Screen) */
    .detective-hint-banner {
      position: absolute;
      left: 21%;
      top: 64%;
      width: 67%;
      background: rgba(255, 255, 255, 0.92);
      border-left: 6px solid #eab308;
      border-radius: clamp(10px, 1.2vw, 16px);
      padding: clamp(8px, 1vw, 14px) clamp(12px, 1.4vw, 20px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      gap: 12px;
      z-index: 15;
    }

    .hint-icon {
      font-size: clamp(1.2rem, 1.8vw, 1.7rem);
      color: #eab308;
      flex-shrink: 0;
    }

    .hint-text {
      font-family: var(--font-main);
      font-size: clamp(0.95rem, 1.35vw, 1.25rem);
      font-weight: 700;
      color: #1e293b;
      line-height: 1.35;
    }

    /* Bottom Right Harita Button on Question Screen */
    .question-map-btn-bottom {
      position: absolute;
      right: 3.5%;
      bottom: 3.5%;
      width: clamp(110px, 13vw, 170px);
      height: clamp(42px, 5vw, 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 25;
    }

    .question-map-btn-bottom .img-btn {
      width: 100%;
      height: 100%;
    }

    /* ========================================================
       FEEDBACK SCREENS (Matches resim/dedektif ai-06.png on ai-11.png)
       ======================================================== */
    .feedback-parchment-body {
      position: absolute;
      left: 17%;
      top: 11%;
      width: 66%;
      height: 78%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      padding: clamp(6px, 1vw, 16px) 0;
      z-index: 15;
    }

    #screen-wrong .feedback-parchment-body {
      top: 29%;
      height: 60%;
      justify-content: space-evenly;
      padding: clamp(4px, 0.8vw, 12px) 0;
    }

    /* Authentic Cloud Frame for Correct Answer (Matches resim/dedektif ai-06.png) */
    .feedback-cloud-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: clamp(8px, 1.2vw, 16px);
      background-image: url('resim/frame_cloud_correct.png');
      background-size: 100% 100%;
      background-repeat: no-repeat;
      background-position: center;
      background-color: transparent;
      border: none;
      padding: clamp(16px, 2.5vw, 32px) clamp(36px, 5.5vw, 76px);
      font-family: var(--font-main);
      font-size: clamp(1.2rem, 2.2vw, 2.1rem);
      font-weight: 900;
      filter: drop-shadow(0 8px 18px rgba(13, 33, 142, 0.25));
      box-sizing: border-box;
      max-width: 95%;
    }

    .cloud-title-blue {
      color: #0c1e5a;
      font-weight: 900;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }

    .cloud-answer-red {
      color: #b91c1c;
      font-weight: 900;
    }

    .feedback-cloud-badge.badge-wrong {
      background-image: none;
      background: linear-gradient(180deg, #fed7aa 0%, #fb923c 100%);
      border: 3px solid #c2410c;
      border-radius: 9999px;
      color: #7c2d12;
      box-shadow: 0 8px 24px rgba(194, 65, 12, 0.4);
      padding: clamp(8px, 1.2vw, 14px) clamp(24px, 3.2vw, 48px);
    }

    /* Explanation Card */
    .feedback-explanation-box {
      width: 90%;
      max-width: 780px;
      background: rgba(255, 255, 255, 0.94);
      border-radius: clamp(12px, 1.5vw, 20px);
      border: 2px solid #e2e8f0;
      padding: clamp(10px, 1.4vw, 18px) clamp(16px, 2.2vw, 28px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
      font-family: var(--font-main);
      font-size: clamp(1.05rem, 1.6vw, 1.45rem);
      color: #0f172a;
      line-height: 1.4;
      font-weight: 700;
    }

    /* Thinking Question Box ("Düşünme sorusu...") */
    .feedback-thinking-box {
      width: 90%;
      max-width: 780px;
      background: #eff6ff;
      border: 2px dashed #3b82f6;
      border-radius: clamp(12px, 1.5vw, 20px);
      padding: clamp(8px, 1.2vw, 16px) clamp(14px, 2vw, 24px);
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.12);
      font-family: var(--font-main);
      font-size: clamp(0.98rem, 1.45vw, 1.3rem);
      color: #1e40af;
      line-height: 1.35;
      font-weight: 700;
    }

    /* Buttons Row */
    .feedback-actions-row {
      display: flex;
      gap: clamp(12px, 2.2vw, 32px);
      justify-content: center;
      align-items: center;
      width: 100%;
    }

    .feedback-actions-row .img-btn {
      height: clamp(44px, 4.8vw, 64px);
    }

    /* ========================================================
       EVALUATION & CERTIFICATE SCREEN (Screen 7 on ai-11.png)
       ======================================================== */
    .eval-parchment-content {
      position: absolute;
      left: 17%;
      top: 10%;
      width: 66%;
      height: 80%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: clamp(4px, 0.8vw, 12px) 0;
      z-index: 15;
    }

    .eval-title {
      font-size: clamp(1.3rem, 2.2vw, 2rem);
      font-weight: 900;
      color: #0c1844;
      text-align: center;
    }

    .eval-items-list {
      width: 96%;
      display: flex;
      flex-direction: column;
      gap: clamp(4px, 0.8vw, 10px);
    }

    .eval-row-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.94);
      border: 2px solid #cbd5e1;
      border-radius: clamp(10px, 1.2vw, 16px);
      padding: clamp(6px, 0.9vw, 12px) clamp(12px, 1.4vw, 20px);
      box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }

    .eval-row-card.row-answered {
      border-color: #22c55e;
      background: #f0fdf4;
    }

    .eval-criterion-text {
      font-family: var(--font-main);
      font-size: clamp(0.92rem, 1.3vw, 1.18rem);
      font-weight: 700;
      color: #1e293b;
      text-align: left;
      flex: 1;
      padding-right: 12px;
    }

    .eval-emojis-group {
      display: flex;
      gap: clamp(6px, 1vw, 12px);
    }

    .emoji-face-btn {
      width: clamp(38px, 4vw, 52px);
      height: clamp(34px, 3.4vw, 44px);
      border-radius: clamp(8px, 1vw, 12px);
      border: 2px solid transparent;
      background: rgba(241, 245, 249, 0.9);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.14s ease, border-color 0.14s ease, background 0.14s ease;
      padding: 2px;
    }

    .emoji-face-btn svg {
      width: 85%;
      height: 85%;
    }

    .emoji-face-btn:hover {
      transform: scale(1.15);
    }

    .emoji-face-btn.selected {
      transform: scale(1.18);
      border-color: #2563eb;
      background: #eff6ff;
      box-shadow: 0 0 12px rgba(37,99,235,0.4);
    }

    /* Certificate / Badge Mini Ribbon */
    .eval-ribbon-badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: linear-gradient(180deg, #fef08a 0%, #facc15 100%);
      border: 2px solid #ca8a04;
      border-radius: 9999px;
      padding: 6px 20px;
      font-weight: 900;
      font-size: clamp(0.95rem, 1.4vw, 1.25rem);
      color: #78350f;
      box-shadow: 0 4px 14px rgba(202, 138, 4, 0.35);
    }

    /* Modal Backdrop & Dialog */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(10, 17, 40, 0.82);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }

    .modal-backdrop.open {
      display: flex;
      animation: modalFade 0.22s ease-out;
    }

    @keyframes modalFade {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }

    .modal-parchment-card {
      background: #fffdf5;
      border: 4px solid #f59e0b;
      border-radius: 28px;
      padding: clamp(20px, 3vw, 36px);
      max-width: 680px;
      width: 100%;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      text-align: left;
      position: relative;
    }

    .modal-parchment-card h2 {
      font-size: clamp(1.4rem, 2.2vw, 2rem);
      color: #0c1844;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .modal-parchment-card ul {
      padding-left: 22px;
      margin-bottom: 22px;
      font-size: clamp(1rem, 1.4vw, 1.2rem);
      color: #1e293b;
      line-height: 1.6;
    }

    .modal-parchment-card li {
      margin-bottom: 10px;
    }

    .modal-close-btn {
      display: block;
      margin: 0 auto;
      height: 48px;
    }

    /* Responsive adjustments for phones in portrait */
    @media (max-width: 768px) and (orientation: portrait) {
      .game-stage {
        aspect-ratio: auto;
        height: 100vh;
        max-height: 100vh;
        border-radius: 0;
      }

      .options-row-container {
        flex-direction: column;
        top: 38%;
        gap: 8px;
      }

      .opt-pill-btn {
        padding: 6px 12px;
      }

      .detective-hint-banner {
        top: 72%;
      }
    }
  </style>
</head>
<body>

  <canvas id="confetti-canvas"></canvas>

  <div class="game-viewport">
    <div class="game-stage" id="game-stage">

      <!-- ========================================================
           SCREEN 1: COVER (resim/dedektif ai-02.png)
           ======================================================== -->
      <section id="screen-cover" class="screen active">
        <!-- Top HUD -->
        <header class="hud-header">
          <div class="hud-left">
            <button class="img-btn hud-btn-img" onclick="playClick(); openModal('modal-bilgi')" title="Bilgi" aria-label="Bilgi">
              <img src="resim/btn_cropped/btn_bilgi.png" alt="Bilgi" />
            </button>
            <button class="img-btn hud-btn-img" onclick="playClick(); openModal('modal-nasil')" title="Nasıl Oynanır?" aria-label="Nasıl Oynanır?">
              <img src="resim/btn_cropped/btn_nasil_oynanir.png" alt="Nasıl Oynanır?" />
            </button>
          </div>
          <div class="hud-right">
            <button class="icon-round-btn" id="sound-btn-cover" onclick="toggleSound()" title="Sesi Aç / Kapat" aria-label="Sesi Aç / Kapat">
              <svg id="sound-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </button>
            <button class="icon-round-btn" onclick="toggleFullscreen()" title="Tam Ekran" aria-label="Tam Ekran">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
              </svg>
            </button>
          </div>
        </header>

        <!-- Maceraya Başla Clickable Hotspot over the original illustrated button -->
        <div class="cover-start-hotspot" onclick="playClick(); showScreen('screen-intro')" title="Maceraya Başla" aria-label="Maceraya Başla"></div>
      </section>


      <!-- ========================================================
           SCREEN 2: INTRO / NASIL OYNANIR? (resim/dedektif ai-04.png)
           ======================================================== -->
      <section id="screen-intro" class="screen">
        <header class="hud-header">
          <div class="hud-left">
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
          </div>
          <div class="hud-right">
            <button class="icon-round-btn" onclick="toggleSound()" title="Sesi Aç / Kapat" aria-label="Sesi Aç / Kapat">
              <svg class="sound-icon-ref" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </button>
          </div>
        </header>

        <div class="intro-bottom-btn">
          <button class="img-btn" onclick="playClick(); showScreen('screen-map')" title="Oyun Haritası" aria-label="Oyun Haritası" style="width: 100%; height: 100%;">
            <img src="resim/btn_cropped/btn_oyun_haritasi.png" alt="Oyun Haritası" />
          </button>
        </div>
      </section>


      <!-- ========================================================
           SCREEN 3: GAME MAP (resim/dedektif ai-03.png)
           ======================================================== -->
      <section id="screen-map" class="screen">
        <header class="hud-header">
          <div class="hud-left">
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
            <button class="img-btn hud-btn-img" onclick="playClick(); openModal('modal-nasil')" title="Nasıl Oynanır?" aria-label="Nasıl Oynanır?">
              <img src="resim/btn_cropped/btn_nasil_oynanir.png" alt="Nasıl Oynanır?" />
            </button>
          </div>
          <div class="hud-right">
            <button class="icon-round-btn" onclick="toggleSound()" title="Sesi Aç / Kapat" aria-label="Sesi Aç / Kapat">
              <svg class="sound-icon-ref" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </button>
            <button class="icon-round-btn" onclick="toggleFullscreen()" title="Tam Ekran" aria-label="Tam Ekran">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
              </svg>
            </button>
          </div>
        </header>

        <!-- 5 Interactive Station Card Hotspots strictly matching card bounds -->
        <div class="map-hotspots-container">
          <!-- Station 1: İşlem Dedektifi -->
          <div class="station-card-hotspot station-spot-1" onclick="startStation(1)" title="1. İşlem Dedektifi">
            <span class="map-station-badge" id="badge-st-1" style="display:none;">⭐ Tamamlandı</span>
          </div>

          <!-- Station 2: Tahmin İstasyonu -->
          <div class="station-card-hotspot station-spot-2" onclick="startStation(2)" title="2. Tahmin İstasyonu">
            <span class="map-station-badge" id="badge-st-2" style="display:none;">⭐ Tamamlandı</span>
          </div>

          <!-- Station 3: Zihinden İşlem Laboratuvarı -->
          <div class="station-card-hotspot station-spot-3" onclick="startStation(3)" title="3. Zihinden İşlem Laboratuvarı">
            <span class="map-station-badge" id="badge-st-3" style="display:none;">⭐ Tamamlandı</span>
          </div>

          <!-- Station 4: Günlük Yaşam Görevi -->
          <div class="station-card-hotspot station-spot-4" onclick="startStation(4)" title="4. Günlük Yaşam Görevi">
            <span class="map-station-badge" id="badge-st-4" style="display:none;">⭐ Tamamlandı</span>
          </div>

          <!-- Station 5: Değerlendirme -->
          <div class="station-card-hotspot station-spot-5" onclick="startStation(5)" title="5. Değerlendirme">
            <span class="map-station-badge" id="badge-st-5" style="display:none;">⭐ Tamamlandı</span>
          </div>
        </div>
      </section>


      <!-- ========================================================
           SCREEN 4: QUESTION (resim/dedektif ai-08.png & ai-10.png)
           ======================================================== -->
      <section id="screen-question" class="screen char-boy">
        <!-- Top Question HUD -->
        <header class="hud-header">
          <div class="hud-left">
            <span class="station-pill-badge" id="q-station-pill">
              <span class="star-icon">★</span>
              <span id="q-station-name">1. İşlem Dedektifi</span>
              <span style="opacity: 0.7;">•</span>
              <span id="q-number-counter">Soru 1 / 10</span>
            </span>
          </div>
          <div class="hud-right">
            <button class="icon-round-btn" id="btn-q-audio" onclick="toggleQuestionAudio()" title="Soruyu Sesli Dinle" aria-label="Soruyu Sesli Dinle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </button>
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
          </div>
        </header>

        <!-- Dashed Question Box on Parchment -->
        <div class="question-box-parchment">
          <div class="q-dashed-card" onclick="toggleQuestionAudio()" title="Soruyu dinlemek için tıkla">
            <div class="q-text-content" id="q-text-display">
              6 + 3 = 9 işleminde 6 ve 3 sayılarına ne ad verilir?
            </div>
            <button class="q-speaker-mini" title="Dinle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 3 Option Pill Buttons (Matching resim/dedektif ai-05.png) -->
        <div class="options-row-container" id="q-options-container">
          <button class="opt-pill-btn" onclick="handleOptionSelect(0)">
            <span class="opt-letter-circle">A</span>
            <span class="opt-text-label">Toplanan</span>
          </button>
          <button class="opt-pill-btn" onclick="handleOptionSelect(1)">
            <span class="opt-letter-circle">B</span>
            <span class="opt-text-label">Toplam</span>
          </button>
          <button class="opt-pill-btn" onclick="handleOptionSelect(2)">
            <span class="opt-letter-circle">C</span>
            <span class="opt-text-label">Fark</span>
          </button>
        </div>

        <!-- Bottom Detective Hint / Thinking Banner -->
        <div class="detective-hint-banner">
          <span class="hint-icon">🔍</span>
          <span class="hint-text" id="q-hint-display">Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.</span>
        </div>

        <!-- Bottom Right Harita Button -->
        <div class="question-map-btn-bottom">
          <button class="img-btn" onclick="playClick(); showScreen('screen-map')" title="Harita" aria-label="Harita">
            <img src="resim/btn_cropped/btn_harita.png" alt="Harita" />
          </button>
        </div>
      </section>


      <!-- ========================================================
           SCREEN 5: FEEDBACK CORRECT (resim/dedektif ai-11.png)
           ======================================================== -->
      <section id="screen-correct" class="screen">
        <header class="hud-header">
          <div class="hud-left">
            <span class="station-pill-badge" style="border-color: #22c55e;">
              <span class="star-icon">✓</span>
              <span>Harika! Doğru düşünüyorsun.</span>
            </span>
            </span>
          </div>
          <div class="hud-right">
            <button class="img-btn hud-btn-img" onclick="playClick(); showScreen('screen-map')" title="Harita" aria-label="Harita">
              <img src="resim/btn_cropped/btn_harita.png" alt="Harita" />
            </button>
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
          </div>
        </header>

        <div class="feedback-parchment-body">
          <!-- Authentic Cloud Frame matching resim/dedektif ai-06.png -->
          <div class="feedback-cloud-badge" id="correct-cloud-badge">
            <span class="cloud-title-blue">DOĞRU CEVAP:</span>
            <span class="cloud-answer-red" id="correct-val-display">Toplanan</span>
          </div>

          <!-- Detailed Pedagogical Explanation -->
          <div class="feedback-explanation-box" id="correct-explanation-text">
            <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Cevabını gerekçesiyle birlikte açıkla.</div>
            Toplama işleminde bir araya getirilen sayılara toplanan denir.
          </div>

          <!-- Detective Thinking Prompt ("Düşünme sorusu...") -->
          <div class="feedback-thinking-box" id="correct-thinking-text">
            💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?
          </div>

          <!-- Action Buttons using Assets -->
          <div class="feedback-actions-row">
            <button class="img-btn" onclick="replayCurrentQuestion()" title="Soruya Dön" aria-label="Soruya Dön">
              <img src="resim/btn_cropped/btn_soruya_don.png" alt="Soruya Dön" />
            </button>
            <button class="img-btn" onclick="goToNextQuestion()" title="Devam Et" aria-label="Devam Et">
              <img src="resim/btn_cropped/btn_devam_et.png" alt="Devam Et" />
            </button>
          </div>
        </div>
      </section>


      <!-- ========================================================
           SCREEN 6: FEEDBACK WRONG / TRY AGAIN (resim/dedektif ai-11.png)
           ======================================================== -->
      <section id="screen-wrong" class="screen">
        <header class="hud-header">
          <div class="hud-left">
            <span class="station-pill-badge" style="border-color: #f97316;">
              <span class="star-icon">🔍</span>
              <span>Bir ipucu daha deneyelim!</span>
            </span>
            </span>
          </div>
          <div class="hud-right">
            <button class="img-btn hud-btn-img" onclick="playClick(); showScreen('screen-map')" title="Harita" aria-label="Harita">
              <img src="resim/btn_cropped/btn_harita.png" alt="Harita" />
            </button>
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
          </div>
        </header>

        <div class="feedback-parchment-body">

          <div class="feedback-explanation-box" id="wrong-explanation-text">
            <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Yanlış cevap, düşünme yolunu gözden geçirmek için fırsattır.</div>
            Toplama işleminde bir araya getirilen sayılara toplanan denir.
          </div>

          <div class="feedback-thinking-box" id="wrong-clue-text">
            🔍 Soruyu yeniden düşün ve tekrar dene.
          </div>

          <div class="feedback-actions-row">
            <button class="img-btn" onclick="retryQuestion()" title="Tekrar Düşün" aria-label="Tekrar Düşün">
              <img src="resim/btn_cropped/btn_tekrar_dusun.png" alt="Tekrar Düşün" />
            </button>
            <button class="img-btn" onclick="goToNextQuestion()" title="Devam Et" aria-label="Devam Et">
              <img src="resim/btn_cropped/btn_devam_et.png" alt="Devam Et" />
            </button>
          </div>
        </div>
      </section>


      <!-- ========================================================
           SCREEN 7: EVALUATION & CERTIFICATE (resim/dedektif ai-11.png)
           ======================================================== -->
      <section id="screen-eval" class="screen">
        <header class="hud-header">
          <div class="hud-left">
            <span class="station-pill-badge">
              <span class="star-icon">🏆</span>
              <span>Başarı Sertifikası</span>
            </span>
          </div>
          <div class="hud-right">
            <button class="img-btn hud-btn-img" onclick="playClick(); showScreen('screen-map')" title="Harita" aria-label="Harita">
              <img src="resim/btn_cropped/btn_harita.png" alt="Harita" />
            </button>
            <button class="icon-round-btn" onclick="playClick(); showScreen('screen-cover')" title="Ana Sayfa" aria-label="Ana Sayfa">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </button>
          </div>
        </header>

        <div class="eval-parchment-content">
          <h2 class="eval-title">Kendimi Değerlendiriyorum</h2>

          <div class="eval-items-list" id="eval-items-container">
            <!-- Populated dynamically with 5 evaluation criteria -->
          </div>

          <div class="eval-ribbon-badge">
            🏅 Tebrikler Dedektif! Tüm İstasyonları Başarıyla Tamamladın!
          </div>

          <div class="feedback-actions-row">
            <button class="img-btn" onclick="playClick(); showScreen('screen-map')" title="Oyun Haritası" aria-label="Oyun Haritası">
              <img src="resim/btn_cropped/btn_oyun_haritasi.png" alt="Oyun Haritası" />
            </button>
            <button class="img-btn" onclick="restartEntireGame()" title="Yeniden Başla" aria-label="Yeniden Başla">
              <img src="resim/btn_cropped/btn_basla.png" alt="Yeniden Başla" />
            </button>
          </div>
        </div>
      </section>

    </div>
  </div>


  <!-- ========================================================
       MODAL: BİLGİ
       ======================================================== -->
  <div id="modal-bilgi" class="modal-backdrop" onclick="closeModalOnBackdrop(event, 'modal-bilgi')">
    <div class="modal-parchment-card">
      <h2>💡 Dedektiflik Bilgi Kartı</h2>
      <ul>
        <li>Bu eğlenceli ve etkileşimli matematik macerası; <strong>toplama ve çıkarma işlemlerine</strong> ilişkin ögeleri belirlemek ve aralarındaki ilişkiyi kavramak amacıyla tasarlanmıştır.</li>
        <li>İşlemleri yapmadan önce <strong>tahmin etme</strong>, sayıları <strong>10'a tamamlama</strong> ve <strong>parçalayarak zihinden çözme</strong> stratejilerini geliştirir.</li>
        <li>Gerçek sonuçlar ile tahmin sonuçları arasında tutarlılığı kontrol ederek problem çözme özgüvenini artırır.</li>
      </ul>
      <button class="img-btn modal-close-btn" onclick="closeModal('modal-bilgi')">
        <img src="resim/btn_cropped/btn_devam_et.png" alt="Anladım" />
      </button>
    </div>
  </div>


  <!-- ========================================================
       MODAL: NASIL OYNANIR?
       ======================================================== -->
  <div id="modal-nasil" class="modal-backdrop" onclick="closeModalOnBackdrop(event, 'modal-nasil')">
    <div class="modal-parchment-card">
      <h2>🗺️ Nasıl Oynanır?</h2>
      <ul>
        <li><strong>1. İpucunu Oku:</strong> Soru kutusundaki işlemi ve soruyu dikkatlice oku veya ses butonuna tıklayarak dinle.</li>
        <li><strong>2. Tahmin Et:</strong> Seçeneklere bakmadan önce sonucun yaklaşık kaç olabileceğini zihninde tahmin et.</li>
        <li><strong>3. Zihinden Çöz:</strong> 10'a tamamlama veya sayıları parçalama yolunu kullanarak doğru cevaba tıkla.</li>
        <li><strong>4. Dedektif Açıklamasını İncele:</strong> Doğru cevap ve düşünme sorusu ile matematik bağlarını keşfet!</li>
        <li><strong>5. Kendini Değerlendir:</strong> 5 istasyon tamamlandığında yüz ifadelerini seçerek dedektiflik rozetini kazan!</li>
      </ul>
      <button class="img-btn modal-close-btn" onclick="closeModal('modal-nasil')">
        <img src="resim/btn_cropped/btn_basla.png" alt="Başla" />
      </button>
    </div>
  </div>


  <!-- ========================================================
       GAME JAVASCRIPT LOGIC & AUDIO SYNTHESIS
       ======================================================== -->
  <script>
    // --- 10 Pedagogical Questions across 5 Stations ---
    const QUESTIONS = [
      {
        station: 1,
        stationName: "1. İşlem Dedektifi",
        questionText: "6 + 3 = 9 işleminde 6 ve 3 sayısına ne ad verilir?",
        options: [
          { letter: "A", text: "Toplanan" },
          { letter: "B", text: "Toplam" },
          { letter: "C", text: "Fark" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: Toplanan",
        explanation: "Toplama işleminde bir araya getirilen sayılara toplanan denir.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "Toplama işleminde bir araya getirilen sayılara toplanan denir.",
        audioFile: "audio/q1.mp3"
      },
      {
        station: 1,
        stationName: "1. İşlem Dedektifi",
        questionText: "12 − 5 = 7 işleminde 7 sayısına ne ad verilir?",
        options: [
          { letter: "A", text: "Çıkan" },
          { letter: "B", text: "Fark" },
          { letter: "C", text: "Eksilen" }
        ],
        correctIndex: 1,
        correctBanner: "DOĞRU CEVAP: Fark",
        explanation: "Çıkarma işleminde elde edilen sonuca fark denir.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "Çıkarma işleminde elde edilen sonuca fark denir.",
        audioFile: "audio/q2.mp3"
      },
      {
        station: 2,
        stationName: "2. Tahmin İstasyonu",
        questionText: "<div class=\"q-math-expr\">8 + 5</div>Deniz verilen toplama işleminin sonucuna hangi tahminde bulunursa gerçek sonuca en yakın tahminde bulunur?",
        options: [
          { letter: "A", text: "10" },
          { letter: "B", text: "12" },
          { letter: "C", text: "20" }
        ],
        correctIndex: 1,
        correctBanner: "DOĞRU CEVAP: 13",
        explanation: "8 + 5 = 13. 8'in üzerine 5 sayarsak 13'e ulaşırız.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "8 + 5 = 13. 8'in üzerine 5 sayarsak 13'e ulaşırız.",
        audioFile: "audio/q3.mp3"
      },
      {
        station: 2,
        stationName: "2. Tahmin İstasyonu",
        questionText: "14 − 6 işleminde fark kaçtır?",
        options: [
          { letter: "A", text: "8" },
          { letter: "B", text: "10" },
          { letter: "C", text: "18" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: 8",
        explanation: "14'ten 6 geri say: 13, 12, 11, 10, 9, 8. Sonuç 8'dir.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "14'ten 6 geri say: 13, 12, 11, 10, 9, 8. Sonuç 8'dir.",
        audioFile: "audio/q4.mp3"
      },
      {
        station: 3,
        stationName: "3. Zihinden İşlem Laboratuvarı",
        questionText: "9 + 4 işlemini 10'a tamamlayarak zihinden bulalım?",
        options: [
          { letter: "A", text: "12" },
          { letter: "B", text: "13" },
          { letter: "C", text: "14" }
        ],
        correctIndex: 1,
        correctBanner: "DOĞRU CEVAP: 13",
        explanation: "4'ün 1'ini 9'a ekleyerek 10 yaparız. 4'ten 3 kalır. 10 + 3 = 13.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "4'ün 1'ini 9'a ekleyerek 10 yaparız. 4'ten 3 kalır. 10 + 3 = 13.",
        audioFile: "audio/q5.mp3"
      },
      {
        station: 3,
        stationName: "3. Zihinden İşlem Laboratuvarı",
        questionText: "16 − 7 işlemini adım adım düşünelim zihinden bulalım?",
        options: [
          { letter: "A", text: "9" },
          { letter: "B", text: "10" },
          { letter: "C", text: "11" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: 9",
        explanation: "7'yi 6 ve 1 olarak ayırırız. 16 − 6 = 10, 10 − 1 = 9.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "7'yi 6 ve 1 olarak ayırırız. 16 − 6 = 10, 10 − 1 = 9.",
        audioFile: "audio/q6.mp3"
      },
      {
        station: 4,
        stationName: "4. Günlük Yaşam Görevi",
        questionText: "Ece'nin 7 bilyesi vardır. Arkadaşı 5 bilye daha verdi. Ece'nin kaç bilyesi oldu?",
        options: [
          { letter: "A", text: "2" },
          { letter: "B", text: "11" },
          { letter: "C", text: "12" }
        ],
        correctIndex: 2,
        correctBanner: "DOĞRU CEVAP: 12",
        explanation: "Bir araya gelme olduğu için toplama yaparız: 7 + 5 = 12.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "Bir araya gelme olduğu için toplama yaparız: 7 + 5 = 12.",
        audioFile: "audio/q7.mp3"
      },
      {
        station: 4,
        stationName: "4. Günlük Yaşam Görevi",
        questionText: "Sepette 15 elma vardır. 4 elmayı yedim. Kaç elma kaldı?",
        options: [
          { letter: "A", text: "11" },
          { letter: "B", text: "19" },
          { letter: "C", text: "10" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: 11",
        explanation: "Azalma olduğu için çıkarma yaparız: 15 − 4 = 11.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "Azalma olduğu için çıkarma yaparız: 15 − 4 = 11.",
        audioFile: "audio/q8.mp3"
      },
      {
        station: 5,
        stationName: "5. Değerlendirme & Tutarlılık",
        questionText: "11 + 6 işlemini Ali 18, Ece 20 tahmin etti. Hangi tahmin gerçek sonuca daha yakındır?",
        options: [
          { letter: "A", text: "Ali'nin 18 tahmini" },
          { letter: "B", text: "Ece'nin 20 tahmini" },
          { letter: "C", text: "İkisi de eşit" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: Ali'nin 18 tahmini",
        explanation: "11 + 6 = 17. Ali'nin tahmini tam sonuca en yakındır.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "11 + 6 = 17. Ali'nin tahmini tam sonuca en yakındır.",
        audioFile: "audio/q9.mp3"
      },
      {
        station: 5,
        stationName: "5. Değerlendirme & Strateji",
        questionText: "8 + 7 işlemini zihinden çözmek için hangi yolu kullanmalıyız?",
        options: [
          { letter: "A", text: "8'i 10 yapmak için 7'den 2 alırım" },
          { letter: "B", text: "8'den 7 çıkarırım" },
          { letter: "C", text: "Sayıları görmezden gelirim" }
        ],
        correctIndex: 0,
        correctBanner: "DOĞRU CEVAP: 8'i 10 yapmak için 7'den 2 alırım",
        explanation: "7'nin 2'sini 8'e verip 10 yaparız; 7'den 2 kalır 5. 10 + 5 = 15.",
        thinkingQuestion: "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?",
        hint: "Cevabı düşün, arkadaşına nasıl düşündüğünü anlat ve seçeneğe tıkla.",
        wrongHint: "7'nin 2'sini 8'e verip 10 yaparız; 7'den 2 kalır 5. 10 + 5 = 15.",
        audioFile: "audio/q10.mp3"
      }
    ];

    const EVAL_ITEMS = [
      "İşlemdeki öğelerin adlarını söyleyebilirim.",
      "Toplama ve çıkarma arasındaki ilişkiyi açıklayabilirim.",
      "İşlem yapmadan önce tahmin edebilirim.",
      "10'a tamamlama veya parçalama stratejisini kullanabilirim.",
      "Sonucun tahminimle tutarlı olup olmadığını kontrol edebilirim."
    ];

    // High quality vector faces for self-evaluation (Evet, Kısmen, Geliştirmeliyim)
    const SVG_HAPPY = `
      <svg viewBox="0 0 48 48">
        <circle cx="24" cy="24" r="22" fill="#fde047" stroke="#eab308" stroke-width="2.5"/>
        <circle cx="16" cy="18" r="3" fill="#0f172a"/>
        <circle cx="32" cy="18" r="3" fill="#0f172a"/>
        <path d="M14 27 C 18 36, 30 36, 34 27" fill="none" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
        <circle cx="11" cy="24" r="2.5" fill="#f87171" opacity="0.6"/>
        <circle cx="37" cy="24" r="2.5" fill="#f87171" opacity="0.6"/>
      </svg>`;

    const SVG_NEUTRAL = `
      <svg viewBox="0 0 48 48">
        <circle cx="24" cy="24" r="22" fill="#fef08a" stroke="#eab308" stroke-width="2.5"/>
        <circle cx="16" cy="18" r="3" fill="#0f172a"/>
        <circle cx="32" cy="18" r="3" fill="#0f172a"/>
        <line x1="16" y1="29" x2="32" y2="29" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
      </svg>`;

    const SVG_THINK = `
      <svg viewBox="0 0 48 48">
        <circle cx="24" cy="24" r="22" fill="#fed7aa" stroke="#f97316" stroke-width="2.5"/>
        <circle cx="16" cy="18" r="3" fill="#0f172a"/>
        <circle cx="32" cy="18" r="3" fill="#0f172a"/>
        <path d="M16 31 Q 24 25, 32 31" fill="none" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
      </svg>`;

    // --- State Variables ---
    let currentQuestionIndex = 0;
    let completedQuestions = new Set();
    let completedStations = new Set();
    let soundEnabled = true;
    let currentQuestionAudio = null;
    let isQuestionAudioPlaying = false;

    // --- Audio Synthesis (Web Audio API) ---
    const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function getAudioCtx() {
      if (!audioCtx && AudioCtxClass) {
        audioCtx = new AudioCtxClass();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume().catch(() => {});
      }
      return audioCtx;
    }

    function playTone(freq, duration, type = 'sine', delay = 0, gainLevel = 0.12) {
      if (!soundEnabled) return;
      try {
        const ctx = getAudioCtx();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime + delay);
        gain.gain.setValueAtTime(gainLevel, ctx.currentTime + delay);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + delay);
        osc.stop(ctx.currentTime + delay + duration);
      } catch (e) {}
    }

    function playClick() {
      playTone(560, 0.08, 'triangle', 0, 0.1);
    }

    function playCorrect() {
      playTone(523.25, 0.12, 'sine', 0, 0.14);     // C5
      playTone(659.25, 0.12, 'sine', 0.09, 0.14);  // E5
      playTone(783.99, 0.22, 'sine', 0.18, 0.16);  // G5
      playTone(1046.5, 0.35, 'sine', 0.28, 0.14);  // C6
    }

    function playWrong() {
      playTone(320, 0.15, 'sawtooth', 0, 0.08);
      playTone(280, 0.22, 'sawtooth', 0.12, 0.08);
    }

    function playFanfare() {
      playTone(523.25, 0.14, 'triangle', 0);
      playTone(659.25, 0.14, 'triangle', 0.12);
      playTone(783.99, 0.14, 'triangle', 0.24);
      playTone(1046.5, 0.45, 'triangle', 0.36);
    }

    function toggleSound() {
      soundEnabled = !soundEnabled;
      const soundSvg = document.getElementById('sound-icon-svg');
      if (soundSvg) {
        if (soundEnabled) {
          soundSvg.innerHTML = `
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>`;
        } else {
          soundSvg.innerHTML = `
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <line x1="23" y1="9" x2="17" y2="15"></line>
            <line x1="17" y1="9" x2="23" y2="15"></line>`;
          stopQuestionAudio();
        }
      }
      playClick();
    }

    function toggleFullscreen() {
      playClick();
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) document.exitFullscreen().catch(() => {});
      }
    }

    // --- Screen Navigation ---
    function showScreen(screenId) {
      stopQuestionAudio();
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(screenId);
      if (target) {
        target.classList.add('active');
      }
    }

    // --- Start Station from Map ---
    function startStation(stationNum) {
      playClick();
      if (stationNum === 5 && completedQuestions.has(8) && completedQuestions.has(9)) {
        showScreen('screen-eval');
      } else {
        const questionIndicesByStation = { 1: 0, 2: 2, 3: 4, 4: 6, 5: 8 };
        loadQuestion(questionIndicesByStation[stationNum]);
      }
    }

    // --- Question Rendering & Interaction ---
    function loadQuestion(index) {
      currentQuestionIndex = index;
      const q = QUESTIONS[index];
      if (!q) return;

      // Update question text and header
      document.getElementById('q-station-name').textContent = q.stationName;
      document.getElementById('q-number-counter').textContent = `Soru ${index + 1} / ${QUESTIONS.length}`;
      const qTextEl = document.getElementById('q-text-display');
      qTextEl.innerHTML = q.questionText;
      document.getElementById('q-hint-display').textContent = q.hint;

      // Natural alternation between boy and girl detectives
      const qScreen = document.getElementById('screen-question');
      qScreen.classList.remove('char-boy', 'char-girl');
      qScreen.classList.add(index % 2 === 0 ? 'char-boy' : 'char-girl');

      // Populate Option Pill Buttons
      const optsContainer = document.getElementById('q-options-container');
      optsContainer.innerHTML = q.options.map((opt, i) => `
        <button class="opt-pill-btn" id="opt-btn-${i}" onclick="handleOptionSelect(${i})" title="${opt.letter} Seçeneği">
          <span class="opt-letter-circle">${opt.letter}</span>
          <span class="opt-text-label">${opt.text}</span>
        </button>
      `).join('');

      showScreen('screen-question');

      // Automatically play audio narration if enabled
      setTimeout(() => {
        playQuestionAudio(index);
      }, 350);
    }

    function handleOptionSelect(optIdx) {
      const q = QUESTIONS[currentQuestionIndex];
      stopQuestionAudio();

            if (optIdx === q.correctIndex) {
        // Correct Answer!
        playCorrect();
        launchConfetti();
        completedQuestions.add(currentQuestionIndex);
        updateStationProgress();

        const answerVal = q.correctBanner.replace(/^DOĞRU CEVAP:\s*/i, '').trim();
        const valEl = document.getElementById('correct-val-display');
        if (valEl) {
          valEl.textContent = answerVal;
        } else {
          document.getElementById('correct-cloud-badge').innerHTML = `<span class="cloud-title-blue">DOĞRU CEVAP:</span> <span class="cloud-answer-red">${answerVal}</span>`;
        }
        document.getElementById('correct-explanation-text').innerHTML = `
          <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Cevabını gerekçesiyle birlikte açıkla.</div>
          ${q.explanation}
        `;
        document.getElementById('correct-thinking-text').innerHTML = q.thinkingQuestion || "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?";

        showScreen('screen-correct');
      } else {
        // Wrong / Try Again
        playWrong();
        document.getElementById('wrong-explanation-text').innerHTML = `
          <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Yanlış cevap, düşünme yolunu gözden geçirmek için fırsattır.</div>
          ${q.wrongHint || q.explanation}
        `;
        document.getElementById('wrong-clue-text').innerHTML = `🔍 Soruyu yeniden düşün ve tekrar dene.`;
        showScreen('screen-wrong');
      }
    }

    function updateStationProgress() {
      // Station 1: Q0, Q1
      if (completedQuestions.has(0) && completedQuestions.has(1)) completedStations.add(1);
      // Station 2: Q2, Q3
      if (completedQuestions.has(2) && completedQuestions.has(3)) completedStations.add(2);
      // Station 3: Q4, Q5
      if (completedQuestions.has(4) && completedQuestions.has(5)) completedStations.add(3);
      // Station 4: Q6, Q7
      if (completedQuestions.has(6) && completedQuestions.has(7)) completedStations.add(4);
      // Station 5: Q8, Q9
      if (completedQuestions.has(8) && completedQuestions.has(9)) completedStations.add(5);

      for (let st = 1; st <= 5; st++) {
        const badge = document.getElementById(`badge-st-${st}`);
        if (badge) {
          badge.style.display = completedStations.has(st) ? 'inline-flex' : 'none';
        }
      }
    }

    function replayCurrentQuestion() {
      playClick();
      loadQuestion(currentQuestionIndex);
    }

    function retryQuestion() {
      playClick();
      loadQuestion(currentQuestionIndex);
    }

    function goToNextQuestion() {
      playClick();
      if (currentQuestionIndex < QUESTIONS.length - 1) {
        loadQuestion(currentQuestionIndex + 1);
      } else {
        // All 10 questions done! Go to Evaluation & Certificate screen
        playFanfare();
        launchConfetti();
        showScreen('screen-eval');
      }
    }

    // --- Audio Narration (MP3 queue) ---
    function playQuestionAudio(index) {
      if (!soundEnabled) return;
      stopQuestionAudio();

      const q = QUESTIONS[index];
      const btn = document.getElementById('btn-q-audio');
      if (btn) btn.classList.add('pulse-active');

      isQuestionAudioPlaying = true;
      currentQuestionAudio = new Audio(q.audioFile);
      currentQuestionAudio.onended = () => {
        isQuestionAudioPlaying = false;
        if (btn) btn.classList.remove('pulse-active');
      };
      currentQuestionAudio.onerror = () => {
        isQuestionAudioPlaying = false;
        if (btn) btn.classList.remove('pulse-active');
      };
      currentQuestionAudio.play().catch(() => {
        isQuestionAudioPlaying = false;
        if (btn) btn.classList.remove('pulse-active');
      });
    }

    function stopQuestionAudio() {
      isQuestionAudioPlaying = false;
      const btn = document.getElementById('btn-q-audio');
      if (btn) btn.classList.remove('pulse-active');
      if (currentQuestionAudio) {
        try {
          currentQuestionAudio.pause();
          currentQuestionAudio.currentTime = 0;
        } catch (e) {}
        currentQuestionAudio = null;
      }
    }

    function toggleQuestionAudio() {
      playClick();
      if (isQuestionAudioPlaying) {
        stopQuestionAudio();
      } else {
        playQuestionAudio(currentQuestionIndex);
      }
    }

    // --- Build Evaluation Rubric ---
    function buildEvaluationList() {
      const container = document.getElementById('eval-items-container');
      container.innerHTML = EVAL_ITEMS.map((item, idx) => `
        <div class="eval-row-card" id="eval-card-${idx}">
          <span class="eval-criterion-text">${item}</span>
          <div class="eval-emojis-group">
            <button class="emoji-face-btn" onclick="selectEvaluationEmoji(this, ${idx})" title="Evet">${SVG_HAPPY}</button>
            <button class="emoji-face-btn" onclick="selectEvaluationEmoji(this, ${idx})" title="Kısmen">${SVG_NEUTRAL}</button>
            <button class="emoji-face-btn" onclick="selectEvaluationEmoji(this, ${idx})" title="Geliştirmeliyim">${SVG_THINK}</button>
          </div>
        </div>
      `).join('');
    }
    buildEvaluationList();

    function selectEvaluationEmoji(btnEl, rowIdx) {
      playClick();
      const parent = btnEl.parentElement;
      parent.querySelectorAll('.emoji-face-btn').forEach(b => b.classList.remove('selected'));
      btnEl.classList.add('selected');
      const row = document.getElementById(`eval-card-${rowIdx}`);
      if (row) row.classList.add('row-answered');
    }

    function restartEntireGame() {
      playClick();
      completedQuestions.clear();
      completedStations.clear();
      document.querySelectorAll('.map-station-badge').forEach(b => b.style.display = 'none');
      document.querySelectorAll('.emoji-face-btn').forEach(b => b.classList.remove('selected'));
      document.querySelectorAll('.eval-row-card').forEach(r => r.classList.remove('row-answered'));
      showScreen('screen-cover');
    }

    // --- Modals ---
    function openModal(id) {
      playClick();
      document.getElementById(id).classList.add('open');
    }

    function closeModal(id) {
      playClick();
      document.getElementById(id).classList.remove('open');
    }

    function closeModalOnBackdrop(event, id) {
      if (event.target.id === id) {
        closeModal(id);
      }
    }

    // --- Confetti Animation ---
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let confettiAnim = null;

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function launchConfetti() {
      const colors = ['#facc15', '#38bdf8', '#2563eb', '#ec4899', '#22c55e', '#a855f7'];
      for (let i = 0; i < 60; i++) {
        particles.push({
          x: window.innerWidth / 2 + (Math.random() - 0.5) * 300,
          y: window.innerHeight / 2 - 60,
          vx: (Math.random() - 0.5) * 16,
          vy: -Math.random() * 14 - 4,
          size: Math.random() * 9 + 6,
          color: colors[Math.floor(Math.random() * colors.length)],
          rot: Math.random() * 360,
          vrot: (Math.random() - 0.5) * 14,
          alpha: 1
        });
      }
      if (!confettiAnim) animateConfetti();
    }

    function animateConfetti() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.36;
        p.rot += p.vrot;
        p.alpha -= 0.014;

        ctx.save();
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rot * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.65);
        ctx.restore();
      });
      particles = particles.filter(p => p.alpha > 0 && p.y < canvas.height + 40);
      if (particles.length > 0) {
        confettiAnim = requestAnimationFrame(animateConfetti);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        confettiAnim = null;
      }
    }

    // Unlock AudioContext on first user interaction
    window.addEventListener('click', () => { getAudioCtx(); }, { once: true });
    window.addEventListener('touchstart', () => { getAudioCtx(); }, { once: true, passive: true });

    // Handle URL parameters for instant testing and screen jumping
    const urlParams = new URLSearchParams(window.location.search);
    const initialScreen = urlParams.get('screen') || 'screen-cover';
    const qParam = parseInt(urlParams.get('q') || '0', 10);
    const hoverParam = urlParams.get('hover');
    if (initialScreen === 'screen-question') {
      loadQuestion(qParam);
    } else if (initialScreen === 'screen-correct') {
      currentQuestionIndex = qParam;
      const q = QUESTIONS[qParam];
      const answerVal = q.correctBanner.replace(/^DOĞRU CEVAP:\s*/i, '').trim();
      const valEl = document.getElementById('correct-val-display');
      if (valEl) valEl.textContent = answerVal;
      document.getElementById('correct-explanation-text').innerHTML = `
        <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Cevabını gerekçesiyle birlikte açıkla.</div>
        ${q.explanation}
      `;
      document.getElementById('correct-thinking-text').innerHTML = q.thinkingQuestion || "💡 Düşünme sorusu: Bu sonuca başka bir yolla ulaşabilir miydin?";
      showScreen('screen-correct');
    } else if (initialScreen === 'screen-wrong') {
      currentQuestionIndex = qParam;
      const q = QUESTIONS[qParam];
      document.getElementById('wrong-explanation-text').innerHTML = `
        <div style="font-size: 0.9em; opacity: 0.85; margin-bottom: 6px;">Yanlış cevap, düşünme yolunu gözden geçirmek için fırsattır.</div>
        ${q.wrongHint || q.explanation}
      `;
      document.getElementById('wrong-clue-text').innerHTML = `🔍 Soruyu yeniden düşün ve tekrar dene.`;
      showScreen('screen-wrong');
    } else {
      showScreen(initialScreen);
    }
    if (hoverParam) {
      setTimeout(() => {
        const el = document.querySelector(`.station-spot-${hoverParam}`);
        if (el) {
          el.style.borderColor = '#facc15';
          el.style.boxShadow = '0 0 20px 4px rgba(250, 204, 21, 0.8), inset 0 0 14px rgba(255, 255, 255, 0.35)';
        }
      }, 150);
    }
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT.strip())

print("Successfully generated index.html with clean UTF-8 encoding!")
