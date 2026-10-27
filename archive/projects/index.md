---
layout: default
title: Projects
description: "Open-source projects by fl0w: Android low-level utilities, automation bots, reverse engineering tools, and web apps."
---

<div class="projects-page-wrap">
  <div class="projects-page-intro">
    <p class="projects-lead">
      Archive of all original open-source software, Android tools, reverse-engineering experiments, and automation utilities.
    </p>
  </div>

  <!-- Filter & Search Bar -->
  <div class="projects-filter-bar">
    <div class="projects-search-box">
      <svg class="search-icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input
        type="search"
        id="project-search-input"
        class="projects-search-input"
        placeholder="Filter projects by name, keyword, or language (e.g. adb, python, reverse engineering)..."
        aria-label="Filter projects"
      >
      <button type="button" id="project-search-clear" class="search-clear-btn" aria-label="Clear filter" style="display:none;">&times;</button>
    </div>

    <div class="projects-category-pills" id="category-pills">
      <button type="button" class="category-pill active" data-category="all">
        All <span class="pill-count">({{ site.data.projects.size }})</span>
      </button>
      <button type="button" class="category-pill" data-category="android tools">
        Android Tools
      </button>
      <button type="button" class="category-pill" data-category="automation">
        Automation
      </button>
      <button type="button" class="category-pill" data-category="reverse engineering">
        Reverse Engineering
      </button>
      <button type="button" class="category-pill" data-category="web tools">
        Web Tools
      </button>
    </div>

    <div class="projects-status-bar">
      <span id="projects-count-display">Showing all {{ site.data.projects.size }} projects</span>
    </div>
  </div>

  <!-- Projects Grid (Data-driven) -->
  <div class="projects-grid" id="projects-grid">
    {% for project in site.data.projects %}
      {% include project_card.html project=project %}
    {% endfor %}
  </div>

  <!-- Empty State -->
  <div id="projects-empty-state" class="projects-empty-state" style="display: none;">
    <p>No projects match your filter.</p>
    <button type="button" class="btn" onclick="resetProjectFilters()">Reset Filters</button>
  </div>
</div>

<script>
  document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("project-search-input");
    const clearBtn = document.getElementById("project-search-clear");
    const categoryPills = document.querySelectorAll("#category-pills .category-pill");
    const cards = document.querySelectorAll("#projects-grid .project-card");
    const countDisplay = document.getElementById("projects-count-display");
    const emptyState = document.getElementById("projects-empty-state");

    let currentCategory = "all";
    let searchQuery = "";

    function filterProjects() {
      let visibleCount = 0;

      cards.forEach(card => {
        const name = card.getAttribute("data-name") || "";
        const cat = card.getAttribute("data-category") || "";
        const lang = card.getAttribute("data-language") || "";
        const topics = card.getAttribute("data-topics") || "";
        const text = (name + " " + cat + " " + lang + " " + topics).toLowerCase();

        const matchesCat = (currentCategory === "all") || (cat === currentCategory);
        const matchesSearch = !searchQuery || text.includes(searchQuery);

        if (matchesCat && matchesSearch) {
          card.style.display = "";
          visibleCount++;
        } else {
          card.style.display = "none";
        }
      });

      countDisplay.textContent = `Showing ${visibleCount} of ${cards.length} projects`;
      emptyState.style.display = visibleCount === 0 ? "block" : "none";
      clearBtn.style.display = searchQuery ? "inline-flex" : "none";
    }

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value.trim().toLowerCase();
        filterProjects();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        searchInput.value = "";
        searchQuery = "";
        filterProjects();
        searchInput.focus();
      });
    }

    categoryPills.forEach(pill => {
      pill.addEventListener("click", () => {
        categoryPills.forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        currentCategory = pill.getAttribute("data-category");
        filterProjects();
      });
    });

    window.resetProjectFilters = function() {
      if (searchInput) searchInput.value = "";
      searchQuery = "";
      currentCategory = "all";
      categoryPills.forEach(p => {
        if (p.getAttribute("data-category") === "all") p.classList.add("active");
        else p.classList.remove("active");
      });
      filterProjects();
    };
  });
</script>
