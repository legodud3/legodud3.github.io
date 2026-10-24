---
title: Introducing charts to the blog
date: 2026-10-15

---

You can now embed nice-looking charts directly in posts using a fenced code block:

```chart
{
  "type": "line",
  "data": {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
    "datasets": [
      {
        "label": "Posts published",
        "data": [3, 5, 2, 7, 4, 6, 8, 5],
        "borderColor": "rgb(75, 192, 192)",
        "tension": 0.3
      },
      {
        "label": "Drafts started",
        "data": [6, 4, 8, 5, 7, 3, 4, 9],
        "borderColor": "rgb(255, 159, 64)",
        "tension": 0.3
      }
    ]
  },
  "options": {
    "responsive": true,
    "maintainAspectRatio": false,
    "plugins": {
      "title": {
        "display": true,
        "text": "Writing activity over time"
      },
      "legend": {
        "position": "bottom"
      }
    },
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Count"
        }
      }
    }
  }
}
```

Bar charts work too:

```chart
{
  "type": "bar",
  "data": {
    "labels": ["Python", "JavaScript", "Go", "Rust", "TypeScript"],
    "datasets": [
      {
        "label": "Lines of code (thousands)",
        "data": [45, 32, 18, 12, 28],
        "backgroundColor": [
          "rgba(255, 99, 132, 0.7)",
          "rgba(54, 162, 235, 0.7)",
          "rgba(255, 206, 86, 0.7)",
          "rgba(75, 192, 192, 0.7)",
          "rgba(153, 102, 255, 0.7)"
        ],
        "borderColor": [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 206, 86)",
          "rgb(75, 192, 192)",
          "rgb(153, 102, 255)"
        ],
        "borderWidth": 1
      }
    ]
  },
  "options": {
    "responsive": true,
    "maintainAspectRatio": false,
    "plugins": {
      "title": {
        "display": true,
        "text": "Language usage by lines of code"
      }
    },
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Thousands of lines"
        }
      }
    }
  }
}
```

And a simple pie chart:

```chart
{
  "type": "doughnut",
  "data": {
    "labels": ["Drafts", "Published", "Archived"],
    "datasets": [{
      "data": [15, 42, 8],
      "backgroundColor": [
        "rgb(255, 159, 64)",
        "rgb(75, 192, 192)",
        "rgb(201, 203, 207)"
      ]
    }]
  },
  "options": {
    "responsive": true,
    "maintainAspectRatio": false,
    "plugins": {
      "title": {
        "display": true,
        "text": "Post status breakdown"
      }
    }
  }
}
```

To add one to your own post, use the **📊 Insert chart** button in the writing desk, or write a fenced block with language `chart` containing a JSON Chart.js config:

````markdown
```chart
{
  "type": "line",
  "data": { ... },
  "options": { ... }
}
```
````

The build script converts these into `<canvas>` elements that Chart.js renders on page load, and charts respect the site's light/dark theme.
