// Animate number safely
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;

    if (start === end) {
        obj.innerText = end + "%";
        return;
    }

    let range = end - start;
    let current = start;
    let increment = end > start ? 1 : -1;
    let stepTime = Math.max(10, Math.abs(Math.floor(duration / range)));

    let timer = setInterval(() => {
        current += increment;
        obj.innerText = current + "%";

        if (current === end) clearInterval(timer);
    }, stepTime);
}

// Convert "artificialintelligence" → "Artificial Intelligence"
function formatText(text) {
    if (!text) return "";

    // Insert space before capital letters (if any)
    text = text.replace(/([a-z])([A-Z])/g, '$1 $2');

    // If fully lowercase joined words → split manually (basic AI trick)
    text = text.replace(/(artificial)(intelligence)/gi, '$1 $2');

    // Capitalize each word
    return text
        .split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        
        
        .join(" ");
}


// Button loading state
function setLoading(isLoading) {
    const btn = document.getElementById("analyzeBtn");
    if (!btn) return;

    if (isLoading) {
        btn.innerText = "Analyzing...";
        btn.disabled = true;
    } else {
        btn.innerText = "🚀 Analyze AI Match";
        btn.disabled = false;
    }
}


// Skill badges
function createBadges(containerId, skills, type) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "";

    if (!skills || skills.length === 0) {
        container.innerHTML = "<span class='empty'>None</span>";
        return;
    }

    skills.forEach(skill => {
        let span = document.createElement("span");
        span.className = "badge " + type;
        span.innerText = skill;
        container.appendChild(span);
    });
}


// Progress bar
function animateProgress(score) {
    const bar = document.getElementById("progressBar");
    if (!bar) return;

    bar.style.width = "0%";

    setTimeout(() => {
        bar.style.width = score + "%";
    }, 200);
}

function setCircularProgress(percent) {

    const circle = document.getElementById("progressRing");

    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = circumference;

    const offset = circumference - (percent / 100) * circumference;
    circle.style.strokeDashoffset = offset;
}

// MAIN FUNCTION
function analyze() {
   

    let skills = document.getElementById("skills")?.value.trim();
    let job = document.getElementById("job")?.value.trim();

    if (!skills || !job) {
        alert("Enter both skills and job description");
        return;
    }

    setLoading(true);

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            skills: skills,
            job: job
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Server error");
        return res.json();
    })
    .then(data => {

        if (!data || typeof data.score === "undefined") {
            throw new Error("Invalid response");
        }

        // LEFT + CENTER PANEL
        animateValue("scoreText", 0, data.score, 800);
        setCircularProgress(data.score);
        animateProgress(data.score);
        
        createBadges("matchedSkills", data.matched, "matched");
        createBadges("missingSkills", data.missing, "missing");

        // TIPS
        const tipsList = document.getElementById("tips");
        if (tipsList) {
            tipsList.innerHTML = "";

            if (data.tips && data.tips.length > 0) {
                data.tips.forEach(tip => {
                    let li = document.createElement("li");
                    li.innerText = tip;
                    tipsList.appendChild(li);
                });
            } else {
                tipsList.innerHTML = "<li>No suggestions needed</li>";
            }
        }
        // RIGHT PANEL INSIGHTS (CORRECT PLACE)
        document.getElementById("skillGapText").innerText = data.skill_gap;
        document.getElementById("strengthText").innerText = data.strength;
        document.getElementById("confidenceText").innerText = data.confidence;
        document.getElementById("decision").innerText = data.decision;
        document.getElementById("seniority").innerText = data.seniority;
        document.getElementById("reason").innerText = data.reason;
    })
    .catch(err => {
        console.error("ERROR:", err);

        const tipsList = document.getElementById("tips");
        if (tipsList) {
            tipsList.innerHTML = "<li>Server error. Try again.</li>";
        }

        alert("Something went wrong. Check backend.");
    })
    .finally(() => {
        setLoading(false);
    });
}