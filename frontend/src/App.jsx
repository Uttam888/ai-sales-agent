import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";
  
// Shared action formatter used across dashboard and lead intelligence views.
const formatAction = (action) =>
  String(action || "Sales Action")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

function App() {
  const [summary, setSummary] = useState(null);
  const [hotLeads, setHotLeads] = useState([]);
  const [pipeline, setPipeline] = useState({});

  // Sales Dashboard Intelligence
  const [dashboardIntelligence, setDashboardIntelligence] = useState(null);
  const [dashboardIntelligenceLoading, setDashboardIntelligenceLoading] = useState(false);
  const [dashboardIntelligenceError, setDashboardIntelligenceError] = useState("");

  // Sales Analytics
  const [salesAnalytics, setSalesAnalytics] = useState(null);
  const [salesAnalyticsLoading, setSalesAnalyticsLoading] = useState(false);
  const [salesAnalyticsError, setSalesAnalyticsError] = useState("");

  // AI Sales Performance Insights
  const [salesPerformance, setSalesPerformance] = useState(null);
  const [salesPerformanceLoading, setSalesPerformanceLoading] = useState(false);
  const [salesPerformanceError, setSalesPerformanceError] = useState("");

  // AI Lead Opportunity Intelligence
  const [leadOpportunities, setLeadOpportunities] = useState([]);
  const [leadOpportunitiesLoading, setLeadOpportunitiesLoading] = useState(false);
  const [leadOpportunitiesError, setLeadOpportunitiesError] = useState("");

  // Historical Sales Action Learning
  const [actionLearning, setActionLearning] = useState(null);
  const [actionLearningLoading, setActionLearningLoading] = useState(false);
  const [actionLearningError, setActionLearningError] = useState("");

  const [leads, setLeads] = useState([]);
  const [leadsLoading, setLeadsLoading] = useState(false);
  const [leadsError, setLeadsError] = useState("");
  const [leadSearch, setLeadSearch] = useState("");
  const [leadStageFilter, setLeadStageFilter] = useState("ALL");
  const [activeView, setActiveView] = useState("dashboard");

  const [properties, setProperties] = useState([]);
  const [propertiesLoading, setPropertiesLoading] = useState(false);
  const [propertiesError, setPropertiesError] = useState("");
  const [propertySearch, setPropertySearch] = useState("");
  const [propertyTypeFilter, setPropertyTypeFilter] = useState("ALL");
  const [propertyAvailabilityFilter, setPropertyAvailabilityFilter] = useState("ALL");
  const [propertyMaxPrice, setPropertyMaxPrice] = useState("");

  const [siteVisits, setSiteVisits] = useState([]);
  const [siteVisitsLoading, setSiteVisitsLoading] = useState(false);
  const [siteVisitsError, setSiteVisitsError] = useState("");
  const [updatingSiteVisitId, setUpdatingSiteVisitId] = useState(null);
  const [siteVisitActionError, setSiteVisitActionError] = useState("");

  const [followUps, setFollowUps] = useState([]);
  const [followUpsLoading, setFollowUpsLoading] = useState(false);
  const [followUpsError, setFollowUpsError] = useState("");
  const [updatingFollowUpId, setUpdatingFollowUpId] = useState(null);
  const [followUpActionError, setFollowUpActionError] = useState("");

  const [activitySearch, setActivitySearch] = useState("");
  const [activityStatusFilter, setActivityStatusFilter] = useState("ALL");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showAddLead, setShowAddLead] = useState(false);

  const [newLead, setNewLead] = useState({
    name: "",
    phone: "",
    requirement: "",
  });

  const [creatingLead, setCreatingLead] = useState(false);
  const [formError, setFormError] = useState("");
  const [formSuccess, setFormSuccess] = useState("");

  const [selectedLead, setSelectedLead] = useState(null);
  const [leadDetailsLoading, setLeadDetailsLoading] = useState(false);

  const [conversations, setConversations] = useState([]);
  const [chatMessage, setChatMessage] = useState("");
  const [sendingMessage, setSendingMessage] = useState(false);
  const [chatError, setChatError] = useState("");

  // Lead activity timeline
  const [leadActivities, setLeadActivities] = useState([]);
  const [leadActivitiesLoading, setLeadActivitiesLoading] = useState(false);
  const [leadActivitiesError, setLeadActivitiesError] = useState("");

  // Next Best Action
  const [nextBestAction, setNextBestAction] = useState(null);
  const [nextBestActionLoading, setNextBestActionLoading] = useState(false);
  const [nextBestActionError, setNextBestActionError] = useState("");

  // Lead Health & Priority
  const [leadHealth, setLeadHealth] = useState(null);
  const [leadHealthLoading, setLeadHealthLoading] = useState(false);
  const [leadHealthError, setLeadHealthError] = useState("");

  // AI Sales Recommendation
  const [salesRecommendation, setSalesRecommendation] = useState(null);
  const [salesRecommendationLoading, setSalesRecommendationLoading] = useState(false);
  const [salesRecommendationError, setSalesRecommendationError] = useState("");

  // Follow-Up Intelligence
  const [followUpIntelligence, setFollowUpIntelligence] = useState(null);
  const [followUpIntelligenceLoading, setFollowUpIntelligenceLoading] = useState(false);
  const [followUpIntelligenceError, setFollowUpIntelligenceError] = useState("");

  const [outcomeFormOpen, setOutcomeFormOpen] = useState(false);
  const [outcomeValueInput, setOutcomeValueInput] = useState("successful");
  const [outcomeNotes, setOutcomeNotes] = useState("");
  const [savingOutcome, setSavingOutcome] = useState(false);

  // Execute AI Sales Action
  const [executingSalesAction, setExecutingSalesAction] = useState(false);
  const [salesActionError, setSalesActionError] = useState("");
  const [salesActionSuccess, setSalesActionSuccess] = useState("");

  // Browser Voice Agent
  const [voiceAgentOpen, setVoiceAgentOpen] = useState(false);
  const [voiceAgentStatus, setVoiceAgentStatus] = useState("IDLE");
  const [voiceTranscript, setVoiceTranscript] = useState("");
  const [voiceResponse, setVoiceResponse] = useState("");
  const [voiceError, setVoiceError] = useState("");
  const [voiceSession, setVoiceSession] = useState(null);
  const [voiceSupported, setVoiceSupported] = useState(true);
  const voiceRecognitionRef = useRef(null);
  const voiceSpeakingRef = useRef(false);

  // Voice call completion / outcome
  const [voiceConversationHistory, setVoiceConversationHistory] = useState([]);
  const [voiceOutcomeOpen, setVoiceOutcomeOpen] = useState(false);
  const [voiceOutcomeValue, setVoiceOutcomeValue] = useState("successful");
  const [voiceOutcomeNotes, setVoiceOutcomeNotes] = useState("");
  const [voiceOutcomeSaving, setVoiceOutcomeSaving] = useState(false);

  const [showFollowUp, setShowFollowUp] = useState(false);

  const [followUpForm, setFollowUpForm] = useState({
    follow_up_date: "",
    message: "",
    notes: "",
  });

  const [schedulingFollowUp, setSchedulingFollowUp] = useState(false);
  const [followUpError, setFollowUpError] = useState("");
  const [followUpSuccess, setFollowUpSuccess] = useState("");

  const pipelineStages = [
    "NEW",
    "CONTACTED",
    "QUALIFIED",
    "PROPERTY_INTEREST",
    "SITE_VISIT",
    "NEGOTIATION",
    "CONVERTED",
  ];

  // ==========================================================
  // LOAD DASHBOARD
  // ==========================================================

  const loadDashboard = async () => {
    setLoading(true);
    setError("");
    setDashboardIntelligenceLoading(true);
    setDashboardIntelligenceError("");

    // Load the core dashboard independently so a temporary intelligence
    // failure can NEVER make the entire dashboard disappear.
    try {
      const [summaryResponse, hotLeadsResponse, pipelineResponse] =
        await Promise.all([
          fetch(`${API_BASE_URL}/api/dashboard/summary`),
          fetch(`${API_BASE_URL}/api/dashboard/hot-leads`),
          fetch(`${API_BASE_URL}/api/dashboard/pipeline`),
        ]);

      if (!summaryResponse.ok || !hotLeadsResponse.ok || !pipelineResponse.ok) {
        throw new Error("Failed to load dashboard data.");
      }

      const [summaryData, hotLeadsData, pipelineData] = await Promise.all([
        summaryResponse.json(),
        hotLeadsResponse.json(),
        pipelineResponse.json(),
      ]);

      setSummary(summaryData);
      setHotLeads(hotLeadsData.leads || []);
      setPipeline(pipelineData.pipeline || {});
    } catch (err) {
      console.error("Dashboard load error:", err);
      setError(
        "Unable to load dashboard data. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }

    // Intelligence is optional. It gets its own error state and does not
    // block the normal dashboard from rendering.
    try {
      const intelligenceResponse = await fetch(
        `${API_BASE_URL}/api/dashboard/intelligence`
      );

      if (!intelligenceResponse.ok) {
        const errorData = await intelligenceResponse.json().catch(() => ({}));
        throw new Error(
          errorData.detail ||
            `Dashboard intelligence returned ${intelligenceResponse.status}.`
        );
      }

      const intelligenceData = await intelligenceResponse.json();
      setDashboardIntelligence(intelligenceData);
    } catch (err) {
      console.error("Dashboard intelligence load error:", err);
      // Keep the last good intelligence on screen if one exists.
      setDashboardIntelligenceError(
        err.message || "Unable to load dashboard intelligence."
      );
    } finally {
      setDashboardIntelligenceLoading(false);
    }

    // Analytics is optional and must never block the main dashboard.
    try {
      setSalesAnalyticsLoading(true);
      setSalesAnalyticsError("");

      const analyticsResponse = await fetch(
        `${API_BASE_URL}/api/dashboard/analytics`
      );

      const analyticsData = await analyticsResponse.json();

      if (!analyticsResponse.ok) {
        throw new Error(
          analyticsData.detail ||
            `Dashboard analytics returned ${analyticsResponse.status}.`
        );
      }

      setSalesAnalytics(analyticsData);
    } catch (err) {
      console.error("Dashboard analytics load error:", err);
      setSalesAnalyticsError(
        err.message || "Unable to load sales analytics."
      );
    } finally {
      setSalesAnalyticsLoading(false);
    }

    // AI Sales Performance is optional and must never block the dashboard.
    try {
      setSalesPerformanceLoading(true);
      setSalesPerformanceError("");

      const performanceResponse = await fetch(
        `${API_BASE_URL}/api/dashboard/performance-insights`
      );

      const performanceData = await performanceResponse.json();

      if (!performanceResponse.ok) {
        throw new Error(
          performanceData.detail ||
            `Sales performance returned ${performanceResponse.status}.`
        );
      }

      setSalesPerformance(performanceData.performance || null);
    } catch (err) {
      console.error("Sales performance load error:", err);
      setSalesPerformanceError(
        err.message || "Unable to load AI sales performance insights."
      );
    } finally {
      setSalesPerformanceLoading(false);
    }
  };
  // ==========================================================
  // LOAD AI LEAD OPPORTUNITIES
  // ==========================================================

  const loadLeadOpportunities = async () => {
    try {
      setLeadOpportunitiesLoading(true);
      setLeadOpportunitiesError("");

      const leadsResponse = await fetch(
        `${API_BASE_URL}/api/leads/`
      );

      const leadsData = await leadsResponse.json();

      if (!leadsResponse.ok) {
        throw new Error(
          leadsData.detail || "Unable to load leads for opportunity analysis."
        );
      }

      const sourceLeads = leadsData.leads || [];

      const results = await Promise.all(
        sourceLeads.map(async (lead) => {
          try {
            const response = await fetch(
              `${API_BASE_URL}/api/leads/${lead.id}/opportunity`
            );

            const data = await response.json();

            if (!response.ok) {
              throw new Error(
                data.detail || `Opportunity analysis failed for lead ${lead.id}.`
              );
            }

            return data;
          } catch (err) {
            console.error(
              `Opportunity analysis error for lead ${lead.id}:`,
              err
            );
            return null;
          }
        })
      );

      const validResults = results.filter(Boolean);

      validResults.sort((a, b) => {
        const priorityRank = {
          URGENT: 4,
          HIGH: 3,
          MEDIUM: 2,
          LOW: 1,
        };

        const priorityDifference =
          (priorityRank[b.action_priority] || 0) -
          (priorityRank[a.action_priority] || 0);

        if (priorityDifference !== 0) {
          return priorityDifference;
        }

        return (
          (b.lead_score || 0) -
          (a.lead_score || 0)
        );
      });

      setLeadOpportunities(validResults);
    } catch (err) {
      console.error("Lead opportunity load error:", err);
      setLeadOpportunitiesError(
        err.message || "Unable to load lead opportunity intelligence."
      );
    } finally {
      setLeadOpportunitiesLoading(false);
    }
  };

  // ==========================================================
  // LOAD HISTORICAL SALES ACTION LEARNING
  // ==========================================================

  const loadActionLearning = async () => {
    try {
      setActionLearningLoading(true);
      setActionLearningError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/action-learning`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load sales action learning."
        );
      }

      setActionLearning(data);
    } catch (err) {
      console.error("Sales action learning load error:", err);
      setActionLearningError(
        err.message || "Unable to load sales action learning."
      );
    } finally {
      setActionLearningLoading(false);
    }
  };


  useEffect(() => {
    loadDashboard();
    loadLeads();
    loadLeadOpportunities();
    loadActionLearning();
  }, []);


  // ==========================================================
  // LOAD ALL LEADS
  // ==========================================================

  const loadLeads = async () => {
    try {
      setLeadsLoading(true);
      setLeadsError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load leads."
        );
      }

      setLeads(data.leads || []);
    } catch (err) {
      console.error(err);

      setLeadsError(
        err.message || "Unable to load leads."
      );
    } finally {
      setLeadsLoading(false);
    }
  };

  // ==========================================================
  // LOAD ALL PROPERTIES
  // ==========================================================

  const loadProperties = async () => {
    try {
      setPropertiesLoading(true);
      setPropertiesError("");

      const response = await fetch(
        `${API_BASE_URL}/api/properties/`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load properties."
        );
      }

      setProperties(data.properties || []);
    } catch (err) {
      console.error(err);
      setPropertiesError(
        err.message || "Unable to load properties."
      );
    } finally {
      setPropertiesLoading(false);
    }
  };


  // ==========================================================
  // LOAD SITE VISITS
  // ==========================================================

  const loadSiteVisits = async () => {
    try {
      setSiteVisitsLoading(true);
      setSiteVisitsError("");

      const response = await fetch(
        `${API_BASE_URL}/api/activity/site-visits`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load site visits."
        );
      }

      setSiteVisits(data.site_visits || []);
    } catch (err) {
      console.error(err);
      setSiteVisitsError(
        err.message || "Unable to load site visits."
      );
    } finally {
      setSiteVisitsLoading(false);
    }
  };


  // ==========================================================
  // COMPLETE SITE VISIT
  // ==========================================================

  const handleCompleteSiteVisit = async (visitId) => {
    if (!visitId || updatingSiteVisitId) {
      return;
    }

    const confirmed = window.confirm(
      "Mark this site visit as completed?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setUpdatingSiteVisitId(visitId);
      setSiteVisitActionError("");

      const response = await fetch(
        `${API_BASE_URL}/api/site-visits/${visitId}/complete`,
        {
          method: "PATCH",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to complete site visit."
        );
      }

      await loadSiteVisits();
      await loadDashboard();
      await loadLeads();
      if (selectedLead) {
        await loadNextBestAction(selectedLead.id);
      }
    } catch (err) {
      console.error(err);
      setSiteVisitActionError(
        err.message || "Unable to complete site visit."
      );
    } finally {
      setUpdatingSiteVisitId(null);
    }
  };


  // ==========================================================
  // LOAD FOLLOW-UPS
  // ==========================================================

  const loadFollowUps = async () => {
    try {
      setFollowUpsLoading(true);
      setFollowUpsError("");

      const response = await fetch(
        `${API_BASE_URL}/api/activity/follow-ups`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load follow-ups."
        );
      }

      setFollowUps(data.follow_ups || []);
    } catch (err) {
      console.error(err);
      setFollowUpsError(
        err.message || "Unable to load follow-ups."
      );
    } finally {
      setFollowUpsLoading(false);
    }
  };


  // ==========================================================
  // COMPLETE FOLLOW-UP
  // ==========================================================

  const handleCompleteFollowUp = async (followUpId) => {
    if (!followUpId || updatingFollowUpId) {
      return;
    }

    const confirmed = window.confirm(
      "Mark this follow-up as completed?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setUpdatingFollowUpId(followUpId);
      setFollowUpActionError("");

      const response = await fetch(
        `${API_BASE_URL}/api/follow-ups/${followUpId}/complete`,
        {
          method: "PATCH",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to complete follow-up."
        );
      }

      await loadFollowUps();
      await loadDashboard();
      await loadLeads();

      if (selectedLead) {
        await loadLeadActivities(selectedLead.id);
      }
    } catch (err) {
      console.error(err);
      setFollowUpActionError(
        err.message || "Unable to complete follow-up."
      );
    } finally {
      setUpdatingFollowUpId(null);
    }
  };


  // ==========================================================
  // CANCEL FOLLOW-UP
  // ==========================================================

  const handleCancelFollowUp = async (followUpId) => {
    if (!followUpId || updatingFollowUpId) {
      return;
    }

    const confirmed = window.confirm(
      "Are you sure you want to cancel this follow-up?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setUpdatingFollowUpId(followUpId);
      setFollowUpActionError("");

      const response = await fetch(
        `${API_BASE_URL}/api/follow-ups/${followUpId}/cancel`,
        {
          method: "PATCH",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to cancel follow-up."
        );
      }

      await loadFollowUps();
      await loadDashboard();
      await loadLeads();

      if (selectedLead) {
        await loadLeadActivities(selectedLead.id);
      }
    } catch (err) {
      console.error(err);
      setFollowUpActionError(
        err.message || "Unable to cancel follow-up."
      );
    } finally {
      setUpdatingFollowUpId(null);
    }
  };

  // ==========================================================
  // ADD NEW LEAD
  // ==========================================================

  const handleCreateLead = async (event) => {
    event.preventDefault();

    setFormError("");
    setFormSuccess("");

    if (!newLead.name.trim()) {
      setFormError("Please enter the lead name.");
      return;
    }

    if (!newLead.phone.trim()) {
      setFormError("Please enter the phone number.");
      return;
    }

    if (!newLead.requirement.trim()) {
      setFormError("Please enter the lead requirement.");
      return;
    }

    try {
      setCreatingLead(true);

      const response = await fetch(
        `${API_BASE_URL}/api/leads/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: newLead.name.trim(),
            phone: newLead.phone.trim(),
            requirement: newLead.requirement.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to create lead."
        );
      }

      setFormSuccess(
        `Lead #${data.lead.id} created successfully.`
      );

      setNewLead({
        name: "",
        phone: "",
        requirement: "",
      });

      await loadDashboard();
      await loadLeads();

      setTimeout(() => {
        setShowAddLead(false);
        setFormSuccess("");
      }, 1200);
    } catch (err) {
      console.error(err);

      setFormError(
        err.message || "Unable to create lead."
      );
    } finally {
      setCreatingLead(false);
    }
  };

  // ==========================================================
  // LOAD LEAD ACTIVITY TIMELINE
  // ==========================================================

  const loadLeadActivities = async (leadId) => {
    try {
      setLeadActivitiesLoading(true);
      setLeadActivitiesError("");

      const response = await fetch(
        `${API_BASE_URL}/api/activity/lead/${leadId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load lead activity."
        );
      }

      setLeadActivities(data.activities || []);
    } catch (err) {
      console.error(err);
      setLeadActivitiesError(
        err.message || "Unable to load lead activity."
      );
      setLeadActivities([]);
    } finally {
      setLeadActivitiesLoading(false);
    }
  };


  // ==========================================================
  // LOAD NEXT BEST ACTION
  // ==========================================================

  const loadNextBestAction = async (leadId) => {
    if (!leadId) {
      return;
    }

    try {
      setNextBestActionLoading(true);
      setNextBestActionError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${leadId}/next-best-action`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load next best action."
        );
      }

      setNextBestAction(data);
    } catch (err) {
      console.error(err);
      setNextBestAction(null);
      setNextBestActionError(
        err.message || "Unable to load next best action."
      );
    } finally {
      setNextBestActionLoading(false);
    }
  };


  // ==========================================================
  // LOAD LEAD HEALTH & PRIORITY
  // ==========================================================

  const loadLeadHealth = async (leadId) => {
    if (!leadId) {
      return;
    }

    try {
      setLeadHealthLoading(true);
      setLeadHealthError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${leadId}/health`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load lead health."
        );
      }

      setLeadHealth(data);
    } catch (err) {
      console.error(err);
      setLeadHealth(null);
      setLeadHealthError(
        err.message || "Unable to load lead health."
      );
    } finally {
      setLeadHealthLoading(false);
    }
  };


  // ==========================================================
  // LOAD AI SALES RECOMMENDATION
  // ==========================================================

  const loadSalesRecommendation = async (leadId) => {
    if (!leadId) {
      return;
    }

    try {
      setSalesRecommendationLoading(true);
      setSalesRecommendationError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${leadId}/sales-recommendation`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load sales recommendation."
        );
      }

      setSalesRecommendation(data);
    } catch (err) {
      console.error(err);
      setSalesRecommendation(null);
      setSalesRecommendationError(
        err.message || "Unable to load sales recommendation."
      );
    } finally {
      setSalesRecommendationLoading(false);
    }
  };


  // ==========================================================
  // LOAD FOLLOW-UP INTELLIGENCE
  // ==========================================================

  const loadFollowUpIntelligence = async (leadId) => {
    if (!leadId) {
      return;
    }

    try {
      setFollowUpIntelligenceLoading(true);
      setFollowUpIntelligenceError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${leadId}/follow-up-intelligence`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load follow-up intelligence."
        );
      }

      setFollowUpIntelligence(data);
    } catch (err) {
      console.error(err);
      setFollowUpIntelligence(null);
      setFollowUpIntelligenceError(
        err.message || "Unable to load follow-up intelligence."
      );
    } finally {
      setFollowUpIntelligenceLoading(false);
    }
  };


  // ==========================================================
  // EXECUTE AI SALES ACTION
  // ==========================================================

  const handleRecordSalesActionOutcome = async () => {
    if (
      !selectedLead ||
      !salesRecommendation?.sales_history?.latest_action_outcome ||
      savingOutcome
    ) {
      return;
    }

    setSavingOutcome(true);
    setSalesActionError("");
    setSalesActionSuccess("");

    const latestOutcome =
      salesRecommendation.sales_history.latest_action_outcome;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/leads/${selectedLead.id}/action-outcome`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: latestOutcome.action,
            outcome: outcomeValueInput,
            notes: outcomeNotes.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail?.message ||
            data.detail ||
            "Unable to record the sales outcome."
        );
      }

      setOutcomeFormOpen(false);
      setOutcomeValueInput("successful");
      setOutcomeNotes("");
      setSalesActionSuccess("Sales outcome recorded successfully.");

      await Promise.all([
        loadSalesRecommendation(selectedLead.id),
        loadLeadActivities(selectedLead.id),
        loadNextBestAction(selectedLead.id),
        loadLeadHealth(selectedLead.id),
        loadFollowUpIntelligence(selectedLead.id),
        loadActionLearning(),
      ]);
    } catch (err) {
      console.error(err);
      setSalesActionError(
        err.message || "Unable to record the sales outcome."
      );
    } finally {
      setSavingOutcome(false);
    }
  };


  const handleExecuteSalesAction = async (action) => {
    if (!selectedLead || !action || executingSalesAction) {
      return;
    }

    setSalesActionError("");
    setSalesActionSuccess("");

    const body = { action };

    // A missed site visit needs the new property and visit date.
    if (action === "contact_and_reschedule_site_visit") {
      const propertyId = window.prompt(
        "Enter the property ID for the new site visit:"
      );

      if (!propertyId) {
        return;
      }

      const visitDate = window.prompt(
        "Enter the new visit date/time (YYYY-MM-DDTHH:MM):",
        "2026-09-01T11:00"
      );

      if (!visitDate) {
        return;
      }

      body.property_id = Number(propertyId);
      body.visit_date = visitDate;
    }

    try {
      setExecutingSalesAction(true);

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${selectedLead.id}/execute-action`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to execute the sales action."
        );
      }

      setSalesActionSuccess(
        data.message || "Sales action executed successfully."
      );

      // Refresh every state that can change after an action.
      await Promise.all([
        loadDashboard(),
        loadLeads(),
        loadSiteVisits(),
        loadFollowUps(),
        loadLeadActivities(selectedLead.id),
        loadNextBestAction(selectedLead.id),
        loadLeadHealth(selectedLead.id),
        loadSalesRecommendation(selectedLead.id),
        loadFollowUpIntelligence(selectedLead.id),
        loadActionLearning(),
      ]);

      // Keep the open lead card in sync with the refreshed lead list.
      const refreshedLead = leads.find(
        (lead) => lead.id === selectedLead.id
      );

      if (refreshedLead) {
        setSelectedLead((current) => ({
          ...current,
          ...refreshedLead,
        }));
      }
    } catch (err) {
      console.error(err);
      setSalesActionError(
        err.message || "Unable to execute the sales action."
      );
    } finally {
      setExecutingSalesAction(false);
    }
  };


  // ==========================================================
  // OPEN LEAD
  // ==========================================================

  const openLead = async (lead) => {
    setSelectedLead(lead);

    setConversations([]);
    setLeadActivities([]);
    setChatMessage("");
    setChatError("");
    setLeadActivitiesError("");
    setNextBestAction(null);
    setNextBestActionError("");
    setLeadHealth(null);
    setLeadHealthError("");
    setSalesRecommendation(null);
    setSalesRecommendationError("");
    setFollowUpIntelligence(null);
    setFollowUpIntelligenceError("");
    setSalesActionError("");
    setSalesActionSuccess("");
    setOutcomeFormOpen(false);
    setOutcomeValueInput("successful");
    setOutcomeNotes("");

    setLeadDetailsLoading(true);

    try {
      const [conversationResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/chat/${lead.id}`),
        loadLeadActivities(lead.id),
        loadNextBestAction(lead.id),
        loadLeadHealth(lead.id),
        loadSalesRecommendation(lead.id),
        loadFollowUpIntelligence(lead.id),
      ]);

      if (!conversationResponse.ok) {
        throw new Error(
          "Unable to load conversation history."
        );
      }

      const data = await conversationResponse.json();

      setConversations(
        data.conversations || []
      );
    } catch (err) {
      console.error(err);

      setChatError(
        err.message ||
          "Unable to load conversation history."
      );
    } finally {
      setLeadDetailsLoading(false);
    }
  };

  // ==========================================================
  // CLOSE LEAD
  // ==========================================================

  const closeLead = () => {
    closeVoiceAgent();
    setSelectedLead(null);
    setConversations([]);
    setLeadActivities([]);
    setLeadActivitiesError("");
    setChatMessage("");
    setChatError("");
    setNextBestAction(null);
    setNextBestActionError("");
    setLeadHealth(null);
    setLeadHealthError("");
    setSalesRecommendation(null);
    setSalesRecommendationError("");
    setSalesActionError("");
    setSalesActionSuccess("");
    setShowFollowUp(false);
  };

  // ==========================================================
  // SEND CHAT MESSAGE
  // ==========================================================

  const handleSendMessage = async (event) => {
    event?.preventDefault();

    const message = chatMessage.trim();

    if (!message || !selectedLead || sendingMessage) {
      return;
    }

    setChatError("");
    setSendingMessage(true);

    const temporaryUserMessage = {
      role: "user",
      message,
      created_at: new Date().toISOString(),
    };

    setConversations((previous) => [
      ...previous,
      temporaryUserMessage,
    ]);

    setChatMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lead_id: selectedLead.id,
            message,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "AI response failed."
        );
      }

      const assistantMessage = {
        role: "assistant",
        message: data.response,
        created_at: new Date().toISOString(),
      };

      setConversations((previous) => [
        ...previous,
        assistantMessage,
      ]);

      if (data.lead) {
        setSelectedLead((previous) => ({
          ...previous,
          ...data.lead,
        }));
      }

      await loadDashboard();
      await loadLeads();
    } catch (err) {
      console.error(err);

      setConversations((previous) =>
        previous.filter(
          (conversation) =>
            conversation !== temporaryUserMessage
        )
      );

      setChatMessage(message);

      setChatError(
        err.message ||
          "Unable to get a response from the AI agent."
      );
    } finally {
      setSendingMessage(false);
    }
  };

  // ==========================================================
  // BROWSER VOICE AGENT
  // ==========================================================

  const stopVoiceRecognition = () => {
    const recognition = voiceRecognitionRef.current;
    if (recognition) {
      try {
        recognition.onend = null;
        recognition.stop();
      } catch {
        // Recognition may already be stopped.
      }
      voiceRecognitionRef.current = null;
    }
  };

  const stopVoiceAgent = () => {
    stopVoiceRecognition();

    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }

    voiceSpeakingRef.current = false;
    setVoiceAgentStatus("IDLE");
  };

  // Record the outcome of the completed voice call using the existing
  // sales-action outcome endpoint. This keeps voice calls inside the
  // same historical learning system as other sales actions.
  const completeVoiceCall = async () => {
    if (!selectedLead || !voiceSession || voiceOutcomeSaving) {
      return;
    }

    // The voice-session endpoint nests the AI action under
    // sales_intelligence. Keep fallbacks for compatibility.
    const action =
      voiceSession?.sales_intelligence?.next_best_action ||
      voiceSession?.next_best_action ||
      salesRecommendation?.next_best_action ||
      "contact_lead";

    const transcript = voiceConversationHistory
      .map((item) => {
        const speaker = item.role === "assistant" ? "AI" : "Customer";
        return `${speaker}: ${item.message}`;
      })
      .join("\n");

    const notes = [
      voiceOutcomeNotes.trim(),
      transcript ? `Voice call transcript:\n${transcript}` : "",
    ]
      .filter(Boolean)
      .join("\n\n");

    try {
      setVoiceOutcomeSaving(true);
      setVoiceError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/${selectedLead.id}/action-outcome`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action,
            outcome: voiceOutcomeValue,
            notes: notes || "Voice Agent call completed.",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail?.message ||
            data.detail ||
            "Unable to record the voice call outcome."
        );
      }

      if (data.lead) {
        setSelectedLead((previous) => ({
          ...previous,
          ...data.lead,
        }));
      }

      // Refresh the CRM/intelligence while the selected lead is still open.
      await Promise.all([
        loadDashboard(),
        loadLeads(),
        loadLeadActivities(selectedLead.id),
        loadNextBestAction(selectedLead.id),
        loadLeadHealth(selectedLead.id),
        loadSalesRecommendation(selectedLead.id),
        loadFollowUpIntelligence(selectedLead.id),
        loadActionLearning(),
      ]);

      setVoiceOutcomeOpen(false);
      setVoiceOutcomeValue("successful");
      setVoiceOutcomeNotes("");

      stopVoiceAgent();
      setVoiceAgentOpen(false);
      setVoiceSession(null);
      setVoiceTranscript("");
      setVoiceResponse("");
      setVoiceConversationHistory([]);
    } catch (err) {
      console.error("Voice call completion error:", err);
      setVoiceError(
        err.message || "Unable to record the voice call outcome."
      );
    } finally {
      setVoiceOutcomeSaving(false);
    }
  };

  const handleEndVoiceCall = () => {
    if (!selectedLead || !voiceSession) {
      closeVoiceAgent();
      return;
    }

    stopVoiceAgent();
    setVoiceOutcomeOpen(true);
  };

  const speakVoiceResponse = (text, startListeningAfter = false) => {
    if (!text || !("speechSynthesis" in window)) {
      if (startListeningAfter) {
        setVoiceAgentStatus("LISTENING");
      }
      return;
    }

    window.speechSynthesis.cancel();
    voiceSpeakingRef.current = true;
    setVoiceAgentStatus("SPEAKING");

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-IN";
    utterance.rate = 0.95;
    utterance.pitch = 1;

    utterance.onend = () => {
      voiceSpeakingRef.current = false;
      if (startListeningAfter) {
        setVoiceAgentStatus("LISTENING");
        setTimeout(() => startVoiceListening(), 250);
      } else {
        setVoiceAgentStatus("IDLE");
      }
    };

    utterance.onerror = () => {
      voiceSpeakingRef.current = false;
      if (startListeningAfter) {
        setVoiceAgentStatus("LISTENING");
        setTimeout(() => startVoiceListening(), 250);
      } else {
        setVoiceAgentStatus("IDLE");
      }
    };

    window.speechSynthesis.speak(utterance);
  };

  const handleVoiceConversation = async (message) => {
    if (!selectedLead || !message.trim()) {
      return;
    }

    setVoiceTranscript(message);
    setVoiceAgentStatus("THINKING");
    setVoiceError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          lead_id: selectedLead.id,
          message: message.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Voice conversation failed.");
      }

      const reply =
        data.response ||
        "I am sorry, I could not generate a response right now.";

      setVoiceResponse(reply);
      setVoiceConversationHistory((previous) => [
        ...previous,
        {
          role: "user",
          message: message.trim(),
          created_at: new Date().toISOString(),
        },
        {
          role: "assistant",
          message: reply,
          created_at: new Date().toISOString(),
        },
      ]);

      if (data.lead) {
        setSelectedLead((previous) => ({
          ...previous,
          ...data.lead,
        }));
      }

      setConversations((previous) => [
        ...previous,
        {
          role: "user",
          message: message.trim(),
          created_at: new Date().toISOString(),
        },
        {
          role: "assistant",
          message: reply,
          created_at: new Date().toISOString(),
        },
      ]);

      await Promise.all([
        loadDashboard(),
        loadLeads(),
        loadNextBestAction(selectedLead.id),
        loadLeadHealth(selectedLead.id),
        loadSalesRecommendation(selectedLead.id),
        loadFollowUpIntelligence(selectedLead.id),
      ]);

      speakVoiceResponse(reply, true);
    } catch (err) {
      console.error("Voice agent error:", err);
      setVoiceError(err.message || "Unable to continue the voice conversation.");
      setVoiceAgentStatus("ERROR");
    }
  };

  const startVoiceListening = () => {
    if (!selectedLead) {
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setVoiceSupported(false);
      setVoiceError(
        "Voice input is not supported by this browser. Try Google Chrome or Microsoft Edge."
      );
      setVoiceAgentStatus("ERROR");
      return;
    }

    stopVoiceRecognition();

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setVoiceAgentStatus("LISTENING");
      setVoiceError("");
    };

    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript?.trim();

      if (transcript) {
        handleVoiceConversation(transcript);
      } else {
        setVoiceAgentStatus("LISTENING");
      }
    };

    recognition.onerror = (event) => {
      if (event.error === "no-speech") {
        setVoiceAgentStatus("LISTENING");
        setTimeout(() => startVoiceListening(), 300);
        return;
      }

      if (event.error === "aborted") {
        return;
      }

      console.error("Voice recognition error:", event.error);
      setVoiceError(`Voice input error: ${event.error}.`);
      setVoiceAgentStatus("ERROR");
    };

    recognition.onend = () => {
      voiceRecognitionRef.current = null;
    };

    voiceRecognitionRef.current = recognition;

    try {
      recognition.start();
    } catch (err) {
      console.error("Unable to start voice recognition:", err);
      setVoiceError("Unable to start the microphone. Please try again.");
      setVoiceAgentStatus("ERROR");
    }
  };

  const startVoiceAgent = async () => {
    if (!selectedLead || voiceAgentStatus === "THINKING" || voiceAgentStatus === "SPEAKING") {
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setVoiceSupported(false);
      setVoiceError(
        "Voice input is not supported by this browser. Try Google Chrome or Microsoft Edge."
      );
      setVoiceAgentStatus("ERROR");
      setVoiceAgentOpen(true);
      return;
    }

    setVoiceSupported(true);
    setVoiceAgentOpen(true);
    setVoiceError("");
    setVoiceTranscript("");
    setVoiceResponse("");
    setVoiceConversationHistory([]);
    setVoiceOutcomeOpen(false);
    setVoiceOutcomeValue("successful");
    setVoiceOutcomeNotes("");
    setVoiceAgentStatus("CONNECTING");

    try {
      const response = await fetch(`${API_BASE_URL}/api/voice/session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          lead_id: selectedLead.id,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail || "Unable to create the voice session."
        );
      }

      setVoiceSession(data.session || null);

      const opening =
        data.voice?.opening_message ||
        salesRecommendation?.suggested_message ||
        `Hi ${selectedLead.name || "there"}, how can I help you today?`;

      setVoiceResponse(opening);
      setVoiceConversationHistory([
        {
          role: "assistant",
          message: opening,
          created_at: new Date().toISOString(),
        },
      ]);
      speakVoiceResponse(opening, true);
    } catch (err) {
      console.error("Voice session error:", err);
      setVoiceError(
        err.message || "Unable to start the voice session."
      );
      setVoiceAgentStatus("ERROR");
    }
  };

  const closeVoiceAgent = () => {
    stopVoiceAgent();
    setVoiceAgentOpen(false);
    setVoiceSession(null);
    setVoiceTranscript("");
    setVoiceResponse("");
    setVoiceConversationHistory([]);
    setVoiceOutcomeOpen(false);
    setVoiceOutcomeValue("successful");
    setVoiceOutcomeNotes("");
    setVoiceError("");
  };

  useEffect(() => {
    return () => {
      stopVoiceRecognition();
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // ==========================================================
  // SCHEDULE FOLLOW-UP
  // ==========================================================

  const handleScheduleFollowUp = async (event) => {
    event.preventDefault();

    if (!selectedLead) {
      return;
    }

    setFollowUpError("");
    setFollowUpSuccess("");

    if (!followUpForm.follow_up_date) {
      setFollowUpError(
        "Please select a follow-up date and time."
      );
      return;
    }

    try {
      setSchedulingFollowUp(true);

      const response = await fetch(
        `${API_BASE_URL}/api/follow-ups`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lead_id: selectedLead.id,
            follow_up_date:
              followUpForm.follow_up_date,
            message:
              followUpForm.message.trim() || null,
            notes:
              followUpForm.notes.trim() || null,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to schedule follow-up."
        );
      }

      setFollowUpSuccess(
        "Follow-up scheduled successfully."
      );

      setFollowUpForm({
        follow_up_date: "",
        message: "",
        notes: "",
      });

      await loadDashboard();

      setTimeout(() => {
        setShowFollowUp(false);
        setFollowUpSuccess("");
      }, 1200);
    } catch (err) {
      console.error(err);

      setFollowUpError(
        err.message ||
          "Unable to schedule follow-up."
      );
    } finally {
      setSchedulingFollowUp(false);
    }
  };

  // ==========================================================
  // FORMAT DATE
  // ==========================================================

  const formatDate = (dateString) => {
    if (!dateString) {
      return "";
    }

    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  const activityIcon = (type) => {
    const icons = {
      lead_created: "＋",
      follow_up: "↗",
      communication: "✉",
      site_visit: "⌖",
    };

    return icons[type] || "•";
  };

  const activityLabel = (type) => {
    const labels = {
      lead_created: "Lead Created",
      follow_up: "Follow-up",
      communication: "Communication",
      site_visit: "Site Visit",
    };

    return labels[type] || "Activity";
  };


  // ==========================================================
  // FILTER CRM LEADS
  // ==========================================================

  const filteredLeads = leads.filter((lead) => {
    const search = leadSearch.trim().toLowerCase();

    const matchesSearch =
      !search ||
      String(lead.name || "").toLowerCase().includes(search) ||
      String(lead.phone || "").toLowerCase().includes(search) ||
      String(lead.location || "").toLowerCase().includes(search) ||
      String(lead.property_type || "").toLowerCase().includes(search);

    const matchesStage =
      leadStageFilter === "ALL" ||
      lead.pipeline_stage === leadStageFilter;

    return matchesSearch && matchesStage;
  });

  // ==========================================================
  // FILTER CRM PROPERTIES
  // ==========================================================

  const propertyTypes = [
    ...new Set(
      properties
        .map((property) => property.property_type)
        .filter(Boolean)
    ),
  ];

  const parsePropertyPriceInLakhs = (price) => {
    if (!price) return null;

    const normalized = String(price)
      .toLowerCase()
      .replace(/,/g, "")
      .replace(/₹/g, "")
      .trim();

    const number = parseFloat(normalized);

    if (Number.isNaN(number)) return null;

    if (normalized.includes("crore")) {
      return number * 100;
    }

    if (normalized.includes("lakh")) {
      return number;
    }

    return number;
  };

  const filteredProperties = properties.filter((property) => {
    const search = propertySearch.trim().toLowerCase();

    const matchesSearch =
      !search ||
      String(property.title || "").toLowerCase().includes(search) ||
      String(property.location || "").toLowerCase().includes(search) ||
      String(property.property_type || "").toLowerCase().includes(search);

    const matchesType =
      propertyTypeFilter === "ALL" ||
      property.property_type === propertyTypeFilter;

    const matchesAvailability =
      propertyAvailabilityFilter === "ALL" ||
      (propertyAvailabilityFilter === "AVAILABLE" && property.available === true) ||
      (propertyAvailabilityFilter === "UNAVAILABLE" && property.available === false);

    const numericMaxPrice = propertyMaxPrice
      ? Number(propertyMaxPrice)
      : null;

    const propertyPrice = parsePropertyPriceInLakhs(property.price);

    const matchesPrice =
      !numericMaxPrice ||
      propertyPrice === null ||
      propertyPrice <= numericMaxPrice;

    return (
      matchesSearch &&
      matchesType &&
      matchesAvailability &&
      matchesPrice
    );
  });


  // ==========================================================
  // FILTER SITE VISITS
  // ==========================================================

  const filteredSiteVisits = siteVisits.filter((visit) => {
    const search = activitySearch.trim().toLowerCase();

    const matchesSearch =
      !search ||
      String(visit.lead_name || "").toLowerCase().includes(search) ||
      String(visit.property_title || "").toLowerCase().includes(search) ||
      String(visit.property_location || "").toLowerCase().includes(search);

    const matchesStatus =
      activityStatusFilter === "ALL" ||
      String(visit.status || "").toUpperCase() ===
        activityStatusFilter;

    return matchesSearch && matchesStatus;
  });


  // ==========================================================
  // FILTER FOLLOW-UPS
  // ==========================================================

  const filteredFollowUps = followUps.filter((followUp) => {
    const search = activitySearch.trim().toLowerCase();

    const matchesSearch =
      !search ||
      String(followUp.lead_name || "").toLowerCase().includes(search) ||
      String(followUp.message || "").toLowerCase().includes(search) ||
      String(followUp.notes || "").toLowerCase().includes(search);

    const matchesStatus =
      activityStatusFilter === "ALL" ||
      String(followUp.status || "").toUpperCase() ===
        activityStatusFilter;

    return matchesSearch && matchesStatus;
  });

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="app">

      {/* ====================================================
          TOP BAR
                  ================================================== */}

      <header className="topbar">

        <div>
          <h1>AI Sales Agent</h1>

          <p>
            Real Estate CRM Dashboard
          </p>
        </div>

        <div className="topbar-nav">
          <button
            className={`nav-button ${
              activeView === "dashboard" ? "active" : ""
            }`}
            onClick={() => setActiveView("dashboard")}
          >
            Dashboard
          </button>

          <button
            className={`nav-button ${
              activeView === "leads" ? "active" : ""
            }`}
            onClick={() => {
              setActiveView("leads");
              loadLeads();
            }}
          >
            Leads
          </button>

          <button
            className={`nav-button ${
              activeView === "properties" ? "active" : ""
            }`}
            onClick={() => {
              setActiveView("properties");
              loadProperties();
            }}
          >
            Properties
          </button>

          <button
            className={`nav-button ${
              activeView === "site_visits" ? "active" : ""
            }`}
            onClick={() => {
              setActiveView("site_visits");
              setSiteVisitActionError("");
              loadSiteVisits();
            }}
          >
            Site Visits
          </button>

          <button
            className={`nav-button ${
              activeView === "follow_ups" ? "active" : ""
            }`}
            onClick={() => {
              setActiveView("follow_ups");
              setFollowUpActionError("");
              loadFollowUps();
            }}
          >
            Follow-ups
          </button>
        </div>

        <div className="topbar-actions">

          <button
            className="refresh-button"
            onClick={loadDashboard}
            disabled={loading}
          >
            Refresh
          </button>

          <button
            className="add-lead-button"
            onClick={() => {
              setFormError("");
              setFormSuccess("");
              setShowAddLead(true);
            }}
          >
            + Add New Lead
          </button>

        </div>

      </header>


      {/* ====================================================
          MAIN DASHBOARD
                  ================================================== */}

      <main className="dashboard">

        {activeView === "site_visits" ? (
          <section className="panel activity-panel">
            <div className="panel-header crm-panel-header">
              <div>
                <h2>Site Visits</h2>
                <p>Manage scheduled property visits across your sales pipeline.</p>
              </div>

              <button
                className="refresh-button"
                onClick={loadSiteVisits}
                disabled={siteVisitsLoading}
              >
                {siteVisitsLoading ? "Loading..." : "Refresh Visits"}
              </button>
            </div>

            <div className="crm-toolbar activity-toolbar">
              <input
                className="crm-search"
                type="text"
                value={activitySearch}
                onChange={(event) => setActivitySearch(event.target.value)}
                placeholder="Search lead or property..."
              />

              <select
                className="crm-filter"
                value={activityStatusFilter}
                onChange={(event) =>
                  setActivityStatusFilter(event.target.value)
                }
              >
                <option value="ALL">All Statuses</option>
                <option value="SCHEDULED">Scheduled</option>
                <option value="COMPLETED">Completed</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>

            {siteVisitsError && (
              <div className="error-card crm-error">
                {siteVisitsError}
              </div>
            )}

            {siteVisitActionError && (
              <div className="error-card crm-error">
                {siteVisitActionError}
              </div>
            )}

            {siteVisitsLoading ? (
              <div className="loading-card crm-loading">
                Loading site visits...
              </div>
            ) : filteredSiteVisits.length === 0 ? (
              <div className="empty-state crm-empty">
                No site visits match your current filters.
              </div>
            ) : (
              <div className="activity-list">
                {filteredSiteVisits.map((visit) => (
                  <article className="activity-card" key={visit.id}>
                    <div className="activity-card-main">
                      <div>
                        <div className="activity-eyebrow">
                          Site Visit #{visit.id}
                        </div>
                        <h3>{visit.lead_name || `Lead #${visit.lead_id}`}</h3>
                        <p className="activity-property">
                          {visit.property_title || "Property unavailable"}
                        </p>
                        <p className="activity-location">
                          {visit.property_location || "Location unavailable"}
                        </p>
                      </div>

                      <span
                        className={`activity-status ${
                          String(visit.status || "").toLowerCase()
                        }`}
                      >
                        {visit.status || "Unknown"}
                      </span>
                    </div>

                    <div className="activity-details">
                      <div>
                        <span>Date & Time</span>
                        <strong>{formatDate(visit.visit_date)}</strong>
                      </div>

                      <div>
                        <span>Property Type</span>
                        <strong>{visit.property_type || "—"}</strong>
                      </div>

                      <div>
                        <span>Price</span>
                        <strong>{visit.property_price || "—"}</strong>
                      </div>
                    </div>

                    {visit.notes && (
                      <div className="activity-notes">
                        <strong>Notes</strong>
                        <p>{visit.notes}</p>
                      </div>
                    )}

                    {String(visit.status || "").toLowerCase() === "scheduled" && (
                      <div className="form-actions">
                        <button
                          type="button"
                          className="submit-lead-button"
                          onClick={() =>
                            handleCompleteSiteVisit(visit.id)
                          }
                          disabled={updatingSiteVisitId === visit.id}
                        >
                          {updatingSiteVisitId === visit.id
                            ? "Completing..."
                            : "Mark Completed"}
                        </button>

                        <button
  type="button"
  className="cancel-button"
  onClick={async () => {
    const confirmed = window.confirm(
      "Are you sure you want to cancel this site visit?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setUpdatingSiteVisitId(visit.id);
      setSiteVisitActionError("");

      const response = await fetch(
        `${API_BASE_URL}/api/site-visits/${visit.id}/cancel`,
        {
          method: "PATCH",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to cancel site visit."
        );
      }

      await loadSiteVisits();
      await loadDashboard();
      await loadLeads();

    } catch (err) {
      console.error(err);

      setSiteVisitActionError(
        err.message || "Unable to cancel site visit."
      );

    } finally {
      setUpdatingSiteVisitId(null);
    }
  }}
  disabled={updatingSiteVisitId === visit.id}
>
  {updatingSiteVisitId === visit.id
    ? "Cancelling..."
    : "Cancel Visit"}
</button>
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </section>
        ) : activeView === "follow_ups" ? (
          <section className="panel activity-panel">
            <div className="panel-header crm-panel-header">
              <div>
                <h2>Follow-ups</h2>
                <p>Track pending and completed customer follow-ups.</p>
              </div>

              <button
                className="refresh-button"
                onClick={loadFollowUps}
                disabled={followUpsLoading}
              >
                {followUpsLoading ? "Loading..." : "Refresh Follow-ups"}
              </button>
            </div>

            <div className="crm-toolbar activity-toolbar">
              <input
                className="crm-search"
                type="text"
                value={activitySearch}
                onChange={(event) => setActivitySearch(event.target.value)}
                placeholder="Search lead or follow-up message..."
              />

              <select
                className="crm-filter"
                value={activityStatusFilter}
                onChange={(event) =>
                  setActivityStatusFilter(event.target.value)
                }
              >
                <option value="ALL">All Statuses</option>
                <option value="PENDING">Pending</option>
                <option value="COMPLETED">Completed</option>
                <option value="FAILED">Failed</option>
              </select>
            </div>

            {followUpsError && (
              <div className="error-card crm-error">
                {followUpsError}
              </div>
            )}

            {followUpActionError && (
              <div className="error-card crm-error">
                {followUpActionError}
              </div>
            )}

            {followUpsLoading ? (
              <div className="loading-card crm-loading">
                Loading follow-ups...
              </div>
            ) : filteredFollowUps.length === 0 ? (
              <div className="empty-state crm-empty">
                No follow-ups match your current filters.
              </div>
            ) : (
              <div className="activity-list">
                {filteredFollowUps.map((followUp) => (
                  <article className="activity-card" key={followUp.id}>
                    <div className="activity-card-main">
                      <div>
                        <div className="activity-eyebrow">
                          Follow-up #{followUp.id}
                        </div>
                        <h3>
                          {followUp.lead_name ||
                            `Lead #${followUp.lead_id}`}
                        </h3>
                        <p className="activity-property">
                          {followUp.message || "No message"}
                        </p>
                      </div>

                      <span
                        className={`activity-status ${
                          String(followUp.status || "").toLowerCase()
                        }`}
                      >
                        {followUp.status || "Unknown"}
                      </span>
                    </div>

                    <div className="activity-details">
                      <div>
                        <span>Scheduled For</span>
                        <strong>
                          {formatDate(followUp.follow_up_date)}
                        </strong>
                      </div>

                      <div>
                        <span>Lead ID</span>
                        <strong>#{followUp.lead_id}</strong>
                      </div>

                      <div>
                        <span>Created</span>
                        <strong>
                          {formatDate(followUp.created_at)}
                        </strong>
                      </div>
                    </div>

                    {followUp.notes && (
                      <div className="activity-notes">
                        <strong>Notes</strong>
                        <p>{followUp.notes}</p>
                      </div>
                    )}

                    {String(followUp.status || "").toLowerCase() === "pending" && (
                      <div className="form-actions">
                        <button
                          type="button"
                          className="submit-lead-button"
                          onClick={() =>
                            handleCompleteFollowUp(followUp.id)
                          }
                          disabled={
                            updatingFollowUpId === followUp.id
                          }
                        >
                          {updatingFollowUpId === followUp.id
                            ? "Completing..."
                            : "Mark Completed"}
                        </button>

                        <button
                          type="button"
                          className="cancel-button"
                          onClick={() =>
                            handleCancelFollowUp(followUp.id)
                          }
                          disabled={
                            updatingFollowUpId === followUp.id
                          }
                        >
                          {updatingFollowUpId === followUp.id
                            ? "Cancelling..."
                            : "Cancel Follow-up"}
                        </button>
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </section>
        ) : activeView === "properties" ? (
          <section className="panel crm-properties-panel">
            <div className="panel-header crm-panel-header">
              <div>
                <h2>Properties</h2>
                <p>
                  Browse and filter properties available to the AI sales agent.
                </p>
              </div>

              <button
                className="refresh-button"
                onClick={loadProperties}
                disabled={propertiesLoading}
              >
                {propertiesLoading ? "Loading..." : "Refresh Properties"}
              </button>
            </div>

            <div className="crm-toolbar property-toolbar">
              <input
                className="crm-search"
                type="text"
                value={propertySearch}
                onChange={(event) => setPropertySearch(event.target.value)}
                placeholder="Search title, location or property type..."
              />

              <select
                className="crm-filter"
                value={propertyTypeFilter}
                onChange={(event) => setPropertyTypeFilter(event.target.value)}
              >
                <option value="ALL">All Types</option>
                {propertyTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>

              <select
                className="crm-filter"
                value={propertyAvailabilityFilter}
                onChange={(event) =>
                  setPropertyAvailabilityFilter(event.target.value)
                }
              >
                <option value="ALL">All Availability</option>
                <option value="AVAILABLE">Available</option>
                <option value="UNAVAILABLE">Unavailable</option>
              </select>

              <input
                className="crm-price-filter"
                type="number"
                min="0"
                value={propertyMaxPrice}
                onChange={(event) => setPropertyMaxPrice(event.target.value)}
                placeholder="Max ₹ lakhs"
              />
            </div>

            {propertiesError && (
              <div className="error-card crm-error">
                {propertiesError}
              </div>
            )}

            {propertiesLoading ? (
              <div className="loading-card crm-loading">
                Loading properties...
              </div>
            ) : filteredProperties.length === 0 ? (
              <div className="empty-state crm-empty">
                No properties match your current filters.
              </div>
            ) : (
              <div className="property-grid">
                {filteredProperties.map((property) => (
                  <article className="property-card" key={property.id}>
                    <div className="property-card-top">
                      <span className="property-id">
                        Property #{property.id}
                      </span>

                      <span
                        className={`availability-badge ${
                          property.available ? "available" : "unavailable"
                        }`}
                      >
                        {property.available ? "Available" : "Unavailable"}
                      </span>
                    </div>

                    <h3>
                      {property.title || "Untitled Property"}
                    </h3>

                    <p className="property-location">
                      {property.location || "Location not specified"}
                    </p>

                    <div className="property-price">
                      {property.price || "Price on request"}
                    </div>

                    <div className="property-meta">
                      <span>{property.property_type || "—"}</span>
                      <span>{property.bedrooms ?? "—"} bed</span>
                      <span>{property.bathrooms ?? "—"} bath</span>
                      <span>
                        {property.area_sqft
                          ? `${property.area_sqft} sq.ft.`
                          : "Area —"}
                      </span>
                    </div>

                    {property.description && (
                      <p className="property-description">
                        {property.description}
                      </p>
                    )}

                    {property.amenities && (
                      <div className="property-amenities">
                        <strong>Amenities</strong>
                        <span>{property.amenities}</span>
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </section>
        ) : activeView === "leads" ? (
          <section className="panel crm-leads-panel">
            <div className="panel-header crm-panel-header">
              <div>
                <h2>Leads</h2>
                <p>
                  Search, filter and manage your complete sales pipeline.
                </p>
              </div>

              <button
                className="add-lead-button"
                onClick={() => {
                  setFormError("");
                  setFormSuccess("");
                  setShowAddLead(true);
                }}
              >
                + Add New Lead
              </button>
            </div>

            <div className="crm-toolbar">
              <input
                className="crm-search"
                type="text"
                value={leadSearch}
                onChange={(event) =>
                  setLeadSearch(event.target.value)
                }
                placeholder="Search name, phone, location or property..."
              />

              <select
                className="crm-filter"
                value={leadStageFilter}
                onChange={(event) =>
                  setLeadStageFilter(event.target.value)
                }
              >
                <option value="ALL">All Stages</option>
                {pipelineStages.map((stage) => (
                  <option key={stage} value={stage}>
                    {stage.replaceAll("_", " ")}
                  </option>
                ))}
              </select>

              <button
                className="refresh-button"
                onClick={loadLeads}
                disabled={leadsLoading}
              >
                {leadsLoading ? "Loading..." : "Refresh Leads"}
              </button>
            </div>

            {leadsError && (
              <div className="error-card crm-error">
                {leadsError}
              </div>
            )}

            {leadsLoading ? (
              <div className="loading-card crm-loading">
                Loading leads...
              </div>
            ) : filteredLeads.length === 0 ? (
              <div className="empty-state crm-empty">
                No leads match your current search or filter.
              </div>
            ) : (
              <div className="lead-table-wrapper">
                <table className="lead-table crm-lead-table">
                  <thead>
                    <tr>
                      <th>Lead</th>
                      <th>Phone</th>
                      <th>Budget</th>
                      <th>Location</th>
                      <th>Property</th>
                      <th>Intent</th>
                      <th>Score</th>
                      <th>Stage</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredLeads.map((lead) => (
                      <tr
                        key={lead.id}
                        className="clickable-lead-row"
                        onClick={() => openLead(lead)}
                      >
                        <td>
                          <div className="lead-name">
                            {lead.name || "Unnamed Lead"}
                          </div>
                          <div className="lead-id">
                            Lead #{lead.id}
                          </div>
                        </td>

                        <td>
                          {lead.phone || "—"}
                        </td>

                        <td>
                          {lead.budget || "—"}
                        </td>

                        <td>
                          {lead.location || "—"}
                        </td>

                        <td>
                          {lead.property_type || "—"}
                        </td>

                        <td>
                          <span
                            className={`intent-badge ${
                              lead.buying_intent || ""
                            }`}
                          >
                            {lead.buying_intent || "—"}
                          </span>
                        </td>

                        <td>
                          <span className="score">
                            {lead.lead_score ?? 0}
                          </span>
                        </td>

                        <td>
                          <span className="stage-badge">
                            {(lead.pipeline_stage || "NEW").replaceAll(
                              "_",
                              " "
                            )}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        ) : (
          <>
        {loading && (
          <div className="loading-card">
            Loading dashboard...
          </div>
        )}

        {error && (
          <div className="error-card">
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          summary && (
            <>

              {/* ==================================================
                  STATS
                  ================================================== */}

              <section className="stats-grid">

                <div className="stat-card">
                  <span>Total Leads</span>
                  <strong>
                    {summary.total_leads}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Hot Leads</span>
                  <strong>
                    {summary.hot_leads}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Qualified</span>
                  <strong>
                    {summary.qualified_leads}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Site Visits</span>
                  <strong>
                    {summary.site_visits}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Pending Follow-ups</span>
                  <strong>
                    {summary.pending_follow_ups}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Converted</span>
                  <strong>
                    {summary.converted_leads}
                  </strong>
                </div>

                <div className="stat-card">
                  <span>Average Score</span>
                  <strong>
                    {summary.average_lead_score}
                  </strong>
                </div>

              </section>


              {/* ==================================================
                  SALES DASHBOARD INTELLIGENCE
                  ================================================== */}

              <section
                className="panel"
                style={{
                  marginBottom: "22px",
                }}
              >
                <div className="panel-header">
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      AI Sales Intelligence
                    </div>

                    <h2>Sales Dashboard Intelligence</h2>

                    <p>
                      A live view of lead health, priority and sales activity.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={loadDashboard}
                    disabled={loading || dashboardIntelligenceLoading}
                  >
                    {dashboardIntelligenceLoading
                      ? "Loading..."
                      : "Refresh"}
                  </button>
                </div>

                {dashboardIntelligenceError && (
                  <div
                    className="error-card"
                    style={{ marginBottom: "16px" }}
                  >
                    {dashboardIntelligenceError}
                  </div>
                )}

                {dashboardIntelligenceLoading && !dashboardIntelligence ? (
                  <div className="loading-card">
                    Loading sales intelligence...
                  </div>
                ) : dashboardIntelligence ? (
                  <>
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(150px, 1fr))",
                        gap: "12px",
                        marginBottom: "18px",
                      }}
                    >
                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#fff7f7",
                          border: "1px solid #fee2e2",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          🔥 Hot Leads
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.health?.hot ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#fffbeb",
                          border: "1px solid #fef3c7",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          🟡 Warm Leads
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.health?.warm ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#f8fafc",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          ⚪ Cold Leads
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.health?.cold ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#fff7ed",
                          border: "1px solid #fed7aa",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          🚨 Urgent
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.priority?.urgent ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#f8fbff",
                          border: "1px solid #dbe3f0",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          High Priority
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.priority?.high ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#f8fbff",
                          border: "1px solid #dbe3f0",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          Pending Follow-ups
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.activities
                            ?.pending_follow_ups ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#f8fbff",
                          border: "1px solid #dbe3f0",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "6px",
                          }}
                        >
                          Scheduled Site Visits
                        </span>
                        <strong style={{ fontSize: "26px" }}>
                          {dashboardIntelligence.activities
                            ?.scheduled_site_visits ?? 0}
                        </strong>
                      </div>
                    </div>

                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(280px, 1fr))",
                        gap: "18px",
                      }}
                    >
                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#f8fafc",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 4px",
                            fontSize: "17px",
                          }}
                        >
                          AI Action Queue
                        </h3>

                        <div
                          style={{
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "14px",
                          }}
                        >
                          Who needs attention first and why.
                        </div>

                        {dashboardIntelligence.top_leads?.length ? (
                          <div
                            style={{
                              display: "grid",
                              gap: "10px",
                            }}
                          >
                            {dashboardIntelligence.top_leads.map((lead) => (
                              <button
                                key={lead.id}
                                type="button"
                                onClick={() => {
                                  const existingLead = leads.find(
                                    (item) => item.id === lead.id
                                  );

                                  openLead(
                                    existingLead || {
                                      id: lead.id,
                                      name: lead.name,
                                      lead_score: lead.lead_score,
                                      pipeline_stage: lead.pipeline_stage,
                                      buying_intent: lead.buying_intent,
                                    }
                                  );
                                }}
                                style={{
                                  width: "100%",
                                  textAlign: "left",
                                  border: "1px solid #e5e7eb",
                                  borderRadius: "10px",
                                  background: "#ffffff",
                                  padding: "12px 14px",
                                  cursor: "pointer",
                                }}
                              >
                                <div
                                  style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    gap: "12px",
                                    alignItems: "center",
                                  }}
                                >
                                  <div>
                                    <strong>{lead.name}</strong>

                                    <div
                                      style={{
                                        fontSize: "12px",
                                        opacity: 0.65,
                                        marginTop: "4px",
                                      }}
                                    >
                                      Lead #{lead.id} •{" "}
                                      {String(
                                        lead.pipeline_stage || "NEW"
                                      ).replaceAll("_", " ")}
                                    </div>

                                    <div
                                      style={{
                                        display: "flex",
                                        alignItems: "center",
                                        gap: "7px",
                                        marginTop: "6px",
                                        flexWrap: "wrap",
                                      }}
                                    >
                                      <span
                                        style={{
                                          fontSize: "10px",
                                          fontWeight: "800",
                                          letterSpacing: "0.04em",
                                          padding: "3px 7px",
                                          borderRadius: "999px",
                                          background:
                                            lead.urgency_level === "ACT NOW"
                                              ? "#fee2e2"
                                              : lead.urgency_level === "DO NEXT"
                                                ? "#fef3c7"
                                                : "#dcfce7",
                                          color:
                                            lead.urgency_level === "ACT NOW"
                                              ? "#b91c1c"
                                              : lead.urgency_level === "DO NEXT"
                                                ? "#92400e"
                                                : "#166534",
                                        }}
                                      >
                                        {lead.urgency_level || "UPCOMING"}
                                      </span>

                                      <span
                                        style={{
                                          fontSize: "10px",
                                          opacity: 0.6,
                                        }}
                                      >
                                        Action score: {lead.action_urgency ?? 0}
                                      </span>
                                    </div>
                                  </div>

                                  <div
                                    style={{
                                      textAlign: "right",
                                    }}
                                  >
                                    <strong>
                                      {lead.lead_score ?? 0}
                                    </strong>

                                    <div
                                      style={{
                                        fontSize: "11px",
                                        marginTop: "3px",
                                        fontWeight: "700",
                                      }}
                                    >
                                      {lead.priority}
                                    </div>
                                  </div>
                                </div>

                                {lead.urgency_reason && (
                                  <div
                                    style={{
                                      fontSize: "12px",
                                      lineHeight: 1.45,
                                      marginTop: "9px",
                                      padding: "8px 10px",
                                      borderRadius: "7px",
                                      background: "#f8fafc",
                                      opacity: 0.82,
                                    }}
                                  >
                                    <strong>Why now:</strong>{" "}
                                    {lead.urgency_reason}
                                  </div>
                                )}

                                {lead.recommended_focus && (
                                  <div
                                    style={{
                                      fontSize: "13px",
                                      lineHeight: 1.5,
                                      opacity: 0.78,
                                      marginTop: "8px",
                                    }}
                                  >
                                    <strong>AI recommends:</strong>{" "}
                                    {lead.recommended_focus}
                                  </div>
                                )}

                                {lead.risks?.length > 0 && (
                                  <div
                                    style={{
                                      fontSize: "12px",
                                      lineHeight: 1.45,
                                      marginTop: "7px",
                                      color: "#b45309",
                                    }}
                                  >
                                    ⚠️ {lead.risks[0]}
                                  </div>
                                )}
                              </button>
                            ))}
                          </div>
                        ) : (
                          <div className="empty-state">
                            No high-priority leads available.
                          </div>
                        )}
                      </div>

                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#f8fbff",
                          border: "1px solid #dbe3f0",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 14px",
                            fontSize: "17px",
                          }}
                        >
                          Activity Snapshot
                        </h3>

                        <div
                          style={{
                            display: "grid",
                            gap: "12px",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              gap: "12px",
                            }}
                          >
                            <span>Pending Follow-ups</span>
                            <strong>
                              {dashboardIntelligence.activities
                                ?.pending_follow_ups ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              gap: "12px",
                            }}
                          >
                            <span>Completed Follow-ups</span>
                            <strong>
                              {dashboardIntelligence.activities
                                ?.completed_follow_ups ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              gap: "12px",
                            }}
                          >
                            <span>Cancelled Follow-ups</span>
                            <strong>
                              {dashboardIntelligence.activities
                                ?.cancelled_follow_ups ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              gap: "12px",
                            }}
                          >
                            <span>Scheduled Site Visits</span>
                            <strong>
                              {dashboardIntelligence.activities
                                ?.scheduled_site_visits ?? 0}
                            </strong>
                          </div>
                        </div>

                        <div
                          style={{
                            marginTop: "18px",
                            paddingTop: "16px",
                            borderTop: "1px solid #dbe3f0",
                            fontSize: "13px",
                            opacity: 0.72,
                            lineHeight: 1.5,
                          }}
                        >
                          {dashboardIntelligence.total_leads ?? 0} total leads
                          are currently being analyzed by the sales
                          intelligence layer.
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="empty-state">
                    No dashboard intelligence is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  AI LEAD OPPORTUNITIES
                  ================================================== */}

              <section
                className="panel"
                style={{
                  marginBottom: "22px",
                }}
              >
                <div className="panel-header">
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      Opportunity Command Center
                    </div>
                    <h2>Top Opportunities &amp; At-Risk Leads</h2>
                    <p>
                      AI identifies which leads deserve attention first and explains why.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={loadLeadOpportunities}
                    disabled={leadOpportunitiesLoading}
                  >
                    {leadOpportunitiesLoading
                      ? "Analyzing..."
                      : "Refresh Opportunities"}
                  </button>
                </div>

                {leadOpportunitiesError && (
                  <div className="error-card" style={{ marginBottom: "16px" }}>
                    {leadOpportunitiesError}
                  </div>
                )}

                {leadOpportunitiesLoading && !leadOpportunities.length ? (
                  <div className="loading-card">
                    Analyzing lead opportunities...
                  </div>
                ) : leadOpportunities.length ? (
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns:
                        "repeat(auto-fit, minmax(300px, 1fr))",
                      gap: "14px",
                    }}
                  >
                    {leadOpportunities
                      .filter((opportunity) =>
                        [
                          "TOP_OPPORTUNITY",
                          "STRONG_OPPORTUNITY",
                          "AT_RISK",
                        ].includes(opportunity.classification)
                      )
                      .slice(0, 6)
                      .map((opportunity) => {
                        const isAtRisk =
                          opportunity.classification === "AT_RISK";
                        const isTop =
                          opportunity.classification === "TOP_OPPORTUNITY";
                        const priority = String(
                          opportunity.action_priority || "LOW"
                        ).toUpperCase();

                        const priorityBackground =
                          priority === "URGENT"
                            ? "#fee2e2"
                            : priority === "HIGH"
                              ? "#fef3c7"
                              : priority === "MEDIUM"
                                ? "#e0f2fe"
                                : "#dcfce7";

                        const priorityColor =
                          priority === "URGENT"
                            ? "#991b1b"
                            : priority === "HIGH"
                              ? "#92400e"
                              : priority === "MEDIUM"
                                ? "#075985"
                                : "#166534";

                        return (
                          <article
                            key={opportunity.lead_id}
                            style={{
                              padding: "18px",
                              borderRadius: "14px",
                              border: isAtRisk
                                ? "1px solid #fecaca"
                                : isTop
                                  ? "1px solid #fde68a"
                                  : "1px solid #e5e7eb",
                              background: isAtRisk ? "#fff7f7" : "#ffffff",
                            }}
                          >
                            <div
                              style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "flex-start",
                                gap: "12px",
                                marginBottom: "12px",
                              }}
                            >
                              <div>
                                <h3 style={{ margin: 0, fontSize: "17px" }}>
                                  {opportunity.lead_name ||
                                    `Lead #${opportunity.lead_id}`}
                                </h3>
                                <div
                                  style={{
                                    marginTop: "5px",
                                    fontSize: "12px",
                                    opacity: 0.65,
                                  }}
                                >
                                  Score {opportunity.lead_score ?? 0}
                                  {" · "}
                                  {opportunity.health || "UNKNOWN"}
                                  {" · "}
                                  {opportunity.buying_intent || "unknown"} intent
                                </div>
                              </div>

                              <span
                                style={{
                                  padding: "5px 9px",
                                  borderRadius: "999px",
                                  fontSize: "10px",
                                  fontWeight: "800",
                                  letterSpacing: "0.05em",
                                  background: priorityBackground,
                                  color: priorityColor,
                                  whiteSpace: "nowrap",
                                }}
                              >
                                {priority}
                              </span>
                            </div>

                            <div
                              style={{
                                display: "inline-flex",
                                padding: "5px 9px",
                                borderRadius: "999px",
                                background: isAtRisk
                                  ? "#fee2e2"
                                  : isTop
                                    ? "#fef3c7"
                                    : "#f1f5f9",
                                color: isAtRisk
                                  ? "#991b1b"
                                  : isTop
                                    ? "#92400e"
                                    : "#334155",
                                fontSize: "10px",
                                fontWeight: "800",
                                letterSpacing: "0.05em",
                                marginBottom: "12px",
                              }}
                            >
                              {String(
                                opportunity.classification || "OPPORTUNITY"
                              ).replaceAll("_", " ")}
                            </div>

                            <p
                              style={{
                                margin: "0 0 12px",
                                fontSize: "13px",
                                lineHeight: 1.55,
                              }}
                            >
                              {opportunity.primary_reason ||
                                "No primary reason available."}
                            </p>

                            <div
                              style={{
                                paddingTop: "12px",
                                borderTop: "1px solid #e5e7eb",
                              }}
                            >
                              <div
                                style={{
                                  fontSize: "11px",
                                  fontWeight: "800",
                                  textTransform: "uppercase",
                                  letterSpacing: "0.06em",
                                  opacity: 0.55,
                                  marginBottom: "5px",
                                }}
                              >
                                Recommended action
                              </div>
                              <div
                                style={{
                                  fontSize: "13px",
                                  lineHeight: 1.5,
                                  fontWeight: "600",
                                }}
                              >
                                {opportunity.recommended_action ||
                                  opportunity.recommended_focus ||
                                  "Review this lead."}
                              </div>
                            </div>
                          </article>
                        );
                      })}
                  </div>
                ) : (
                  <div className="empty-state">
                    No opportunity intelligence is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  HISTORICAL SALES ACTION LEARNING
                  ================================================== */}

              <section
                className="panel"
                style={{
                  marginBottom: "22px",
                }}
              >
                <div className="panel-header">
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      AI Learning Layer
                    </div>
                    <h2>Sales Action Learning</h2>
                    <p>
                      Historical customer outcomes help identify which sales actions
                      are producing positive results.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={loadActionLearning}
                    disabled={actionLearningLoading}
                  >
                    {actionLearningLoading ? "Learning..." : "Refresh Learning"}
                  </button>
                </div>

                {actionLearningError && (
                  <div className="error-card" style={{ marginBottom: "16px" }}>
                    {actionLearningError}
                  </div>
                )}

                {actionLearningLoading && !actionLearning ? (
                  <div className="loading-card">
                    Analyzing historical sales outcomes...
                  </div>
                ) : actionLearning ? (
                  <>
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(160px, 1fr))",
                        gap: "12px",
                        marginBottom: "16px",
                      }}
                    >
                      {[
                        [
                          "Historical Outcomes",
                          actionLearning.total_outcomes ?? 0,
                        ],
                        [
                          "Decided Outcomes",
                          actionLearning.decided_outcomes ?? 0,
                        ],
                        [
                          "Positive Rate",
                          `${actionLearning.overall_positive_rate ?? 0}%`,
                        ],
                        [
                          "Actions Learned",
                          actionLearning.action_count ?? 0,
                        ],
                      ].map(([label, value]) => (
                        <div
                          key={label}
                          style={{
                            padding: "15px",
                            borderRadius: "11px",
                            background: "#f8fafc",
                            border: "1px solid #e5e7eb",
                          }}
                        >
                          <div
                            style={{
                              fontSize: "11px",
                              fontWeight: "800",
                              textTransform: "uppercase",
                              letterSpacing: "0.05em",
                              opacity: 0.58,
                              marginBottom: "6px",
                            }}
                          >
                            {label}
                          </div>
                          <div
                            style={{
                              fontSize: "24px",
                              fontWeight: "800",
                            }}
                          >
                            {value}
                          </div>
                        </div>
                      ))}
                    </div>

                    {actionLearning.best_action && (
                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "11px",
                          background: "#eff6ff",
                          border: "1px solid #bfdbfe",
                          marginBottom: "16px",
                        }}
                      >
                        <div
                          style={{
                            fontSize: "11px",
                            fontWeight: "800",
                            textTransform: "uppercase",
                            letterSpacing: "0.05em",
                            color: "#1d4ed8",
                            marginBottom: "5px",
                          }}
                        >
                          Best Historical Action
                        </div>
                        <strong>
                          {formatAction(actionLearning.best_action.action)}
                        </strong>
                        <span style={{ marginLeft: "10px", fontSize: "12px" }}>
                          {actionLearning.best_action.positive_rate ?? 0}% positive
                          outcomes ·{" "}
                          {actionLearning.best_action.sample_size ?? 0} decided
                          outcomes
                        </span>
                      </div>
                    )}

                    {Object.keys(actionLearning.action_performance || {}).length >
                    0 ? (
                      <div
                        style={{
                          display: "grid",
                          gridTemplateColumns:
                            "repeat(auto-fit, minmax(280px, 1fr))",
                          gap: "12px",
                        }}
                      >
                        {Object.entries(
                          actionLearning.action_performance || {}
                        )
                          .sort(
                            (a, b) =>
                              (b[1].positive_rate || 0) -
                              (a[1].positive_rate || 0)
                          )
                          .map(([action, stats]) => (
                            <article
                              key={action}
                              style={{
                                padding: "16px",
                                borderRadius: "12px",
                                background: "#ffffff",
                                border: "1px solid #e5e7eb",
                              }}
                            >
                              <div
                                style={{
                                  display: "flex",
                                  justifyContent: "space-between",
                                  gap: "10px",
                                  marginBottom: "12px",
                                }}
                              >
                                <strong>{formatAction(action)}</strong>
                                <span
                                  style={{
                                    padding: "4px 8px",
                                    borderRadius: "999px",
                                    background:
                                      (stats.positive_rate || 0) >= 70
                                        ? "#dcfce7"
                                        : (stats.positive_rate || 0) >= 40
                                          ? "#fef3c7"
                                          : "#fee2e2",
                                    fontSize: "11px",
                                    fontWeight: "800",
                                  }}
                                >
                                  {stats.positive_rate ?? 0}% positive
                                </span>
                              </div>

                              <div
                                style={{
                                  display: "grid",
                                  gridTemplateColumns:
                                    "repeat(4, minmax(0, 1fr))",
                                  gap: "8px",
                                }}
                              >
                                {[
                                  ["Total", stats.total ?? 0],
                                  ["Successful", stats.successful ?? 0],
                                  ["Progressing", stats.progressing ?? 0],
                                  ["Pending", stats.pending ?? 0],
                                ].map(([label, value]) => (
                                  <div key={label}>
                                    <div
                                      style={{
                                        fontSize: "10px",
                                        opacity: 0.55,
                                        textTransform: "uppercase",
                                        fontWeight: "700",
                                      }}
                                    >
                                      {label}
                                    </div>
                                    <div
                                      style={{
                                        fontWeight: "800",
                                        marginTop: "2px",
                                      }}
                                    >
                                      {value}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </article>
                          ))}
                      </div>
                    ) : (
                      <div className="empty-state">
                        No historical sales action outcomes are available yet.
                      </div>
                    )}
                  </>
                ) : (
                  <div className="empty-state">
                    No sales action learning is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  SALES ANALYTICS
                  ================================================== */}

              <section
                className="panel"
                style={{
                  marginBottom: "22px",
                }}
              >
                <div className="panel-header">
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      Performance Overview
                    </div>

                    <h2>Sales Analytics</h2>

                    <p>
                      Conversion, pipeline and sales execution performance.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={loadDashboard}
                    disabled={loading || salesAnalyticsLoading}
                  >
                    {salesAnalyticsLoading
                      ? "Loading..."
                      : "Refresh Analytics"}
                  </button>
                </div>

                {salesAnalyticsError && (
                  <div
                    className="error-card"
                    style={{ marginBottom: "16px" }}
                  >
                    {salesAnalyticsError}
                  </div>
                )}

                {salesAnalyticsLoading && !salesAnalytics ? (
                  <div className="loading-card">
                    Loading sales analytics...
                  </div>
                ) : salesAnalytics ? (
                  <>
                    {/* KPI CARDS */}
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(170px, 1fr))",
                        gap: "12px",
                        marginBottom: "18px",
                      }}
                    >
                      {[
                        {
                          label: "Total Leads",
                          value: salesAnalytics.leads?.total ?? 0,
                        },
                        {
                          label: "Converted",
                          value: salesAnalytics.leads?.converted ?? 0,
                        },
                        {
                          label: "Conversion Rate",
                          value: `${salesAnalytics.leads?.conversion_rate ?? 0}%`,
                        },
                        {
                          label: "Average Lead Score",
                          value: salesAnalytics.leads?.average_score ?? 0,
                        },
                        {
                          label: "Sales Actions",
                          value: salesAnalytics.sales_actions?.total ?? 0,
                        },
                        {
                          label: "Action Success Rate",
                          value: `${salesAnalytics.sales_actions?.success_rate ?? 0}%`,
                        },
                      ].map((item) => (
                        <div
                          key={item.label}
                          style={{
                            padding: "16px",
                            borderRadius: "12px",
                            background: "#f8fafc",
                            border: "1px solid #e5e7eb",
                          }}
                        >
                          <span
                            style={{
                              display: "block",
                              fontSize: "12px",
                              opacity: 0.65,
                              marginBottom: "6px",
                            }}
                          >
                            {item.label}
                          </span>

                          <strong style={{ fontSize: "25px" }}>
                            {item.value}
                          </strong>
                        </div>
                      ))}
                    </div>

                    {/* PIPELINE + EXECUTION */}
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(280px, 1fr))",
                        gap: "18px",
                      }}
                    >
                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#ffffff",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 14px",
                            fontSize: "17px",
                          }}
                        >
                          Pipeline Performance
                        </h3>

                        <div
                          style={{
                            display: "grid",
                            gap: "10px",
                          }}
                        >
                          {[
                            ["NEW", "New"],
                            ["CONTACTED", "Contacted"],
                            ["QUALIFIED", "Qualified"],
                            ["PROPERTY_INTEREST", "Property Interest"],
                            ["SITE_VISIT", "Site Visit"],
                            ["NEGOTIATION", "Negotiation"],
                            ["CONVERTED", "Converted"],
                          ].map(([key, label]) => (
                            <div
                              key={key}
                              style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                gap: "12px",
                              }}
                            >
                              <span>{label}</span>
                              <strong>
                                {salesAnalytics.pipeline?.[key] ?? 0}
                              </strong>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#ffffff",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 14px",
                            fontSize: "17px",
                          }}
                        >
                          Sales Execution
                        </h3>

                        <div
                          style={{
                            display: "grid",
                            gap: "10px",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Pending Outcomes</span>
                            <strong>
                              {salesAnalytics.sales_actions?.pending ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Successful Outcomes</span>
                            <strong>
                              {salesAnalytics.sales_actions?.successful ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Progressing</span>
                            <strong>
                              {salesAnalytics.sales_actions?.progressing ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Negative Outcomes</span>
                            <strong>
                              {salesAnalytics.sales_actions?.negative ?? 0}
                            </strong>
                          </div>
                        </div>
                      </div>

                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#ffffff",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 14px",
                            fontSize: "17px",
                          }}
                        >
                          Follow-up Performance
                        </h3>

                        <div
                          style={{
                            display: "grid",
                            gap: "10px",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Total Follow-ups</span>
                            <strong>
                              {salesAnalytics.follow_ups?.total ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Completed</span>
                            <strong>
                              {salesAnalytics.follow_ups?.completed ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Pending</span>
                            <strong>
                              {salesAnalytics.follow_ups?.pending ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Completion Rate</span>
                            <strong>
                              {salesAnalytics.follow_ups?.completion_rate ?? 0}%
                            </strong>
                          </div>
                        </div>
                      </div>

                      <div
                        style={{
                          padding: "18px",
                          borderRadius: "12px",
                          background: "#ffffff",
                          border: "1px solid #e5e7eb",
                        }}
                      >
                        <h3
                          style={{
                            margin: "0 0 14px",
                            fontSize: "17px",
                          }}
                        >
                          Site Visit Performance
                        </h3>

                        <div
                          style={{
                            display: "grid",
                            gap: "10px",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Total Visits</span>
                            <strong>
                              {salesAnalytics.site_visits?.total ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Scheduled</span>
                            <strong>
                              {salesAnalytics.site_visits?.scheduled ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Completed</span>
                            <strong>
                              {salesAnalytics.site_visits?.completed ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Cancelled</span>
                            <strong>
                              {salesAnalytics.site_visits?.cancelled ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                            }}
                          >
                            <span>Completion Rate</span>
                            <strong>
                              {salesAnalytics.site_visits?.completion_rate ?? 0}%
                            </strong>
                          </div>
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="empty-state">
                    No sales analytics are currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  AI SALES PERFORMANCE INSIGHTS
                  ================================================== */}

              <section
                className="panel"
                style={{
                  marginBottom: "22px",
                }}
              >
                <div className="panel-header">
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      Management Intelligence
                    </div>

                    <h2>AI Sales Performance</h2>

                    <p>
                      AI-generated insights from conversion, pipeline,
                      follow-up and sales-action performance.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={loadDashboard}
                    disabled={loading || salesPerformanceLoading}
                  >
                    {salesPerformanceLoading
                      ? "Loading..."
                      : "Refresh Insights"}
                  </button>
                </div>

                {salesPerformanceError && (
                  <div
                    className="error-card"
                    style={{ marginBottom: "16px" }}
                  >
                    {salesPerformanceError}
                  </div>
                )}

                {salesPerformanceLoading && !salesPerformance ? (
                  <div className="loading-card">
                    Loading AI sales performance...
                  </div>
                ) : salesPerformance ? (
                  <>
                    {/* OVERALL RECOMMENDATION */}
                    <div
                      style={{
                        padding: "18px",
                        borderRadius: "14px",
                        border: "1px solid #e5e7eb",
                        background: "#f8fafc",
                        marginBottom: "18px",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "flex-start",
                          gap: "16px",
                          flexWrap: "wrap",
                        }}
                      >
                        <div style={{ flex: "1 1 420px" }}>
                          <div
                            style={{
                              fontSize: "11px",
                              fontWeight: "800",
                              letterSpacing: "0.08em",
                              textTransform: "uppercase",
                              opacity: 0.6,
                              marginBottom: "7px",
                            }}
                          >
                            Overall Focus
                          </div>

                          <h3
                            style={{
                              margin: "0 0 8px",
                              fontSize: "20px",
                            }}
                          >
                            {salesPerformance.overall_focus ||
                              "Review current sales performance"}
                          </h3>

                          <p
                            style={{
                              margin: 0,
                              lineHeight: 1.6,
                              opacity: 0.8,
                            }}
                          >
                            {salesPerformance.overall_recommendation ||
                              "No recommendation is currently available."}
                          </p>
                        </div>

                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "flex-end",
                            gap: "8px",
                          }}
                        >
                          <span
                            style={{
                              display: "inline-flex",
                              alignItems: "center",
                              padding: "6px 10px",
                              borderRadius: "999px",
                              fontSize: "11px",
                              fontWeight: "800",
                              letterSpacing: "0.06em",
                              background:
                                String(
                                  salesPerformance.overall_priority || ""
                                ).toUpperCase() === "HIGH"
                                  ? "#fee2e2"
                                  : "#fef3c7",
                              color:
                                String(
                                  salesPerformance.overall_priority || ""
                                ).toUpperCase() === "HIGH"
                                  ? "#991b1b"
                                  : "#92400e",
                            }}
                          >
                            {salesPerformance.overall_priority || "INFO"} PRIORITY
                          </span>

                          <span
                            style={{
                              fontSize: "13px",
                              opacity: 0.65,
                            }}
                          >
                            {salesPerformance.insight_count ?? 0} insights ·{" "}
                            {salesPerformance.high_priority_count ?? 0} high priority
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* INSIGHT CARDS */}
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(280px, 1fr))",
                        gap: "14px",
                      }}
                    >
                      {(salesPerformance.insights || []).map(
                        (insight, index) => {
                          const priority = String(
                            insight.priority || "LOW"
                          ).toUpperCase();

                          const type = String(
                            insight.type || "info"
                          ).toLowerCase();

                          const isHigh = priority === "HIGH";
                          const isMedium = priority === "MEDIUM";

                          return (
                            <article
                              key={`${insight.category || "insight"}-${
                                insight.title || index
                              }-${index}`}
                              style={{
                                padding: "16px",
                                borderRadius: "12px",
                                border: "1px solid #e5e7eb",
                                background: "#ffffff",
                              }}
                            >
                              <div
                                style={{
                                  display: "flex",
                                  justifyContent: "space-between",
                                  alignItems: "center",
                                  gap: "10px",
                                  marginBottom: "12px",
                                }}
                              >
                                <span
                                  style={{
                                    fontSize: "11px",
                                    fontWeight: "800",
                                    letterSpacing: "0.06em",
                                    textTransform: "uppercase",
                                    opacity: 0.55,
                                  }}
                                >
                                  {String(
                                    insight.category || "general"
                                  ).replaceAll("_", " ")}
                                </span>

                                <span
                                  style={{
                                    padding: "4px 8px",
                                    borderRadius: "999px",
                                    fontSize: "10px",
                                    fontWeight: "800",
                                    background: isHigh
                                      ? "#fee2e2"
                                      : isMedium
                                        ? "#fef3c7"
                                        : "#dcfce7",
                                    color: isHigh
                                      ? "#991b1b"
                                      : isMedium
                                        ? "#92400e"
                                        : "#166534",
                                  }}
                                >
                                  {priority}
                                </span>
                              </div>

                              <div
                                style={{
                                  display: "flex",
                                  alignItems: "flex-start",
                                  gap: "10px",
                                }}
                              >
                                <span
                                  aria-hidden="true"
                                  style={{
                                    fontSize: "20px",
                                    lineHeight: 1,
                                  }}
                                >
                                  {type === "positive"
                                    ? "✓"
                                    : type === "warning"
                                      ? "⚠"
                                      : "ℹ"}
                                </span>

                                <div>
                                  <h3
                                    style={{
                                      margin: "0 0 7px",
                                      fontSize: "16px",
                                    }}
                                  >
                                    {insight.title || "Sales insight"}
                                  </h3>

                                  <p
                                    style={{
                                      margin: 0,
                                      lineHeight: 1.55,
                                      fontSize: "14px",
                                      opacity: 0.78,
                                    }}
                                  >
                                    {insight.message ||
                                      "No additional details available."}
                                  </p>
                                </div>
                              </div>
                            </article>
                          );
                        }
                      )}
                    </div>

                    {(salesPerformance.insights || []).length === 0 && (
                      <div className="empty-state">
                        No performance insights are currently available.
                      </div>
                    )}
                  </>
                ) : (
                  <div className="empty-state">
                    No AI sales performance data is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  PIPELINE
                  ================================================== */}

              <section className="panel">

                <div className="panel-header">

                  <div>
                    <h2>
                      Sales Pipeline
                    </h2>

                    <p>
                      Current distribution of your leads
                    </p>
                  </div>

                </div>


                <div className="pipeline">

                  {pipelineStages.map(
                    (stage) => (

                      <div
                        className="pipeline-stage"
                        key={stage}
                      >

                        <span className="stage-name">
                          {stage.replaceAll(
                            "_",
                            " "
                          )}
                        </span>

                        <strong>
                          {pipeline[stage] || 0}
                        </strong>

                      </div>

                    )
                  )}

                </div>

              </section>


              {/* ==================================================
                  HOT LEADS
                  ================================================== */}

              <section className="panel">

                <div className="panel-header">

                  <div>
                    <h2>
                      Hot Leads
                    </h2>

                    <p>
                      Leads with a score of 70 or higher
                    </p>
                  </div>

                </div>


                {hotLeads.length === 0 ? (

                  <div className="empty-state">
                    No hot leads available.
                  </div>

                ) : (

                  <div className="lead-table-wrapper">

                    <table className="lead-table">

                      <thead>

                        <tr>
                          <th>Lead</th>
                          <th>Budget</th>
                          <th>Location</th>
                          <th>Property</th>
                          <th>Intent</th>
                          <th>Score</th>
                          <th>Stage</th>
                        </tr>

                      </thead>


                      <tbody>

                        {hotLeads.map(
                          (lead) => (

                            <tr
                              key={lead.id}
                              className="clickable-lead-row"
                              onClick={() =>
                                openLead(lead)
                              }
                            >

                              <td>

                                <div className="lead-name">
                                  {lead.name ||
                                    "Unnamed Lead"}
                                </div>

                                <div className="lead-id">
                                  Lead #{lead.id}
                                </div>

                              </td>

                              <td>
                                {lead.budget ||
                                  "â€”"}
                              </td>

                              <td>
                                {lead.location ||
                                  "â€”"}
                              </td>

                              <td>
                                {lead.property_type ||
                                  "â€”"}
                              </td>

                              <td>

                                <span
                                  className={`intent-badge ${
                                    lead.buying_intent ||
                                    ""
                                  }`}
                                >
                                  {lead.buying_intent ||
                                    "â€”"}
                                </span>

                              </td>

                              <td>

                                <span className="score">
                                  {lead.lead_score}
                                </span>

                              </td>

                              <td>

                                <span className="stage-badge">
                                  {(
                                    lead.pipeline_stage ||
                                    "NEW"
                                  ).replaceAll(
                                    "_",
                                    " "
                                  )}
                                </span>

                              </td>

                            </tr>

                          )
                        )}

                      </tbody>

                    </table>

                  </div>

                )}

              </section>

            </>
          )}
          </>
        )}

      </main>


      {/* ======================================================
          ADD LEAD MODAL
                  ================================================== */}

      {showAddLead && (

        <div
          className="modal-overlay"
          onMouseDown={(event) => {

            if (
              event.target === event.currentTarget &&
              !creatingLead
            ) {
              setShowAddLead(false);
            }

          }}
        >

          <div className="modal">

            <div className="modal-header">

              <div>

                <h2>
                  Add New Lead
                </h2>

                <p>
                  Enter the customer's requirement.
                  AI will qualify the lead automatically.
                </p>

              </div>

              <button
                className="close-button"
                onClick={() =>
                  setShowAddLead(false)
                }
                disabled={creatingLead}
              >
                Ã—
              </button>

            </div>


            <form
              className="lead-form"
              onSubmit={handleCreateLead}
            >

              {formError && (
                <div className="form-error">
                  {formError}
                </div>
              )}

              {formSuccess && (
                <div className="form-success">
                  {formSuccess}
                </div>
              )}


              <div className="form-group">

                <label>
                  Name
                </label>

                <input
                  type="text"
                  value={newLead.name}
                  onChange={(event) =>
                    setNewLead({
                      ...newLead,
                      name: event.target.value,
                    })
                  }
                  placeholder="Rahul Sharma"
                  disabled={creatingLead}
                />

              </div>


              <div className="form-group">

                <label>
                  Phone
                </label>

                <input
                  type="tel"
                  value={newLead.phone}
                  onChange={(event) =>
                    setNewLead({
                      ...newLead,
                      phone: event.target.value,
                    })
                  }
                  placeholder="9876543210"
                  disabled={creatingLead}
                />

              </div>


              <div className="form-group">

                <label>
                  Requirement
                </label>

                <textarea
                  value={newLead.requirement}
                  onChange={(event) =>
                    setNewLead({
                      ...newLead,
                      requirement:
                        event.target.value,
                    })
                  }
                  placeholder="I am looking for a 3BHK apartment in Noida. My budget is around 1.2 crore and I want to buy within 6 months for self use."
                  rows={5}
                  disabled={creatingLead}
                />

                <small>
                  AI will extract budget,
                  location, property type,
                  purpose, timeline and
                  buying intent.
                </small>

              </div>


              <div className="form-actions">

                <button
                  type="button"
                  className="cancel-button"
                  onClick={() =>
                    setShowAddLead(false)
                  }
                  disabled={creatingLead}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="submit-lead-button"
                  disabled={creatingLead}
                >
                  {creatingLead
                    ? "Qualifying..."
                    : "Create & Qualify Lead"}
                </button>

              </div>

            </form>

          </div>

        </div>

      )}


      {/* ======================================================
          LEAD DETAILS + AI CHAT
                  ================================================== */}

      {selectedLead && (

        <div
          className="modal-overlay"
          onMouseDown={(event) => {

            if (
              event.target === event.currentTarget &&
              !sendingMessage
            ) {
              closeLead();
            }

          }}
        >

          <div className="modal lead-details-modal">

            <div className="modal-header">

              <div>

                <h2>
                  {selectedLead.name ||
                    "Lead Details"}
                </h2>

                <p>
                  Lead #{selectedLead.id}
                  {" â€¢ "}
                  {selectedLead.pipeline_stage ||
                    "NEW"}
                </p>

              </div>

              <button
                className="close-button"
                onClick={closeLead}
                disabled={sendingMessage}
              >
                Ã—
              </button>

            </div>


            <div className="lead-details-content">

              {/* ==================================================
                  LEAD SUMMARY
                  ================================================== */}

              <div className="lead-details-title">

                <div>
                  <h3>
                    Lead Overview
                  </h3>

                  <span>
                    AI-qualified customer
                  </span>
                </div>

                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    flexWrap: "wrap",
                    justifyContent: "flex-end",
                  }}
                >
                  <button
                    type="button"
                    className="submit-lead-button"
                    onClick={startVoiceAgent}
                    disabled={voiceAgentStatus === "CONNECTING" || voiceAgentStatus === "THINKING" || voiceAgentStatus === "SPEAKING"}
                  >
                    🎙️ Talk to Customer
                  </button>

                  <button
                    className="schedule-follow-up-button"
                    onClick={() => {
                      setFollowUpError("");
                      setFollowUpSuccess("");
                      setShowFollowUp(true);
                    }}
                  >
                    + Schedule Follow-up
                  </button>
                </div>

              </div>


              <div className="lead-details-grid">

                <div className="detail-item">
                  <span>Phone</span>
                  <strong>
                    {selectedLead.phone ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Budget</span>
                  <strong>
                    {selectedLead.budget ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Location</span>
                  <strong>
                    {selectedLead.location ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Property</span>
                  <strong>
                    {selectedLead.property_type ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Purpose</span>
                  <strong>
                    {selectedLead.purpose ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Timeline</span>
                  <strong>
                    {selectedLead.timeline ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Buying Intent</span>
                  <strong>
                    {selectedLead.buying_intent ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Qualification</span>
                  <strong>
                    {selectedLead.qualification_status ||
                      "Not provided"}
                  </strong>
                </div>

                <div className="detail-item">
                  <span>Lead Score</span>
                  <strong>
                    {selectedLead.lead_score ?? 0}
                  </strong>
                </div>

              </div>

              {/* ==================================================
                  BROWSER VOICE AGENT
                  ================================================== */}
              {voiceAgentOpen && (
                <section
                  style={{
                    marginTop: "22px",
                    marginBottom: "22px",
                    padding: "20px 22px",
                    border: "1px solid #c7d2fe",
                    borderRadius: "14px",
                    background: "#f8f7ff",
                    boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      gap: "14px",
                      flexWrap: "wrap",
                    }}
                  >
                    <div>
                      <div
                        style={{
                          fontSize: "12px",
                          fontWeight: "800",
                          letterSpacing: "0.08em",
                          textTransform: "uppercase",
                          opacity: 0.65,
                          marginBottom: "5px",
                        }}
                      >
                        AI Voice Agent
                      </div>
                      <h3 style={{ margin: 0, fontSize: "20px" }}>
                        Voice Conversation
                      </h3>
                      <p
                        style={{
                          margin: "6px 0 0",
                          fontSize: "13px",
                          opacity: 0.7,
                        }}
                      >
                        Speak with {selectedLead.name || "the customer"} using
                        your browser microphone.
                      </p>
                    </div>

                    <span
                      style={{
                        padding: "7px 11px",
                        borderRadius: "999px",
                        background:
                          voiceAgentStatus === "LISTENING"
                            ? "#dcfce7"
                            : voiceAgentStatus === "SPEAKING"
                            ? "#dbeafe"
                            : voiceAgentStatus === "THINKING"
                            ? "#fef3c7"
                            : voiceAgentStatus === "ERROR"
                            ? "#fee2e2"
                            : "#e5e7eb",
                        fontSize: "11px",
                        fontWeight: "800",
                      }}
                    >
                      {voiceAgentStatus}
                    </span>
                  </div>

                  {!voiceSupported && (
                    <div
                      className="error-card"
                      style={{ marginTop: "14px" }}
                    >
                      Voice input is not available in this browser. Please
                      use Google Chrome or Microsoft Edge.
                    </div>
                  )}

                  {voiceError && (
                    <div
                      className="error-card"
                      style={{ marginTop: "14px" }}
                    >
                      {voiceError}
                    </div>
                  )}

                  <div
                    style={{
                      marginTop: "16px",
                      display: "grid",
                      gap: "12px",
                    }}
                  >
                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#ffffff",
                      }}
                    >
                      <span
                        style={{
                          display: "block",
                          fontSize: "11px",
                          opacity: 0.6,
                          marginBottom: "5px",
                          fontWeight: "700",
                        }}
                      >
                        YOU SAID
                      </span>
                      <p style={{ margin: 0, lineHeight: 1.55 }}>
                        {voiceTranscript || "Waiting for your voice..."}
                      </p>
                    </div>

                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#ffffff",
                      }}
                    >
                      <span
                        style={{
                          display: "block",
                          fontSize: "11px",
                          opacity: 0.6,
                          marginBottom: "5px",
                          fontWeight: "700",
                        }}
                      >
                        AI RESPONSE
                      </span>
                      <p style={{ margin: 0, lineHeight: 1.55 }}>
                        {voiceResponse || "The AI response will appear here."}
                      </p>
                    </div>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: "8px",
                      flexWrap: "wrap",
                      marginTop: "14px",
                    }}
                  >
                    <button
                      type="button"
                      className="submit-lead-button"
                      onClick={startVoiceListening}
                      disabled={
                        !voiceSupported ||
                        voiceAgentStatus === "CONNECTING" ||
                        voiceAgentStatus === "THINKING" ||
                        voiceAgentStatus === "SPEAKING"
                      }
                    >
                      🎙️ Listen
                    </button>

                    <button
                      type="button"
                      className="cancel-button"
                      onClick={handleEndVoiceCall}
                      disabled={
                        !voiceSession ||
                        voiceOutcomeSaving ||
                        voiceAgentStatus === "CONNECTING"
                      }
                    >
                      End Call
                    </button>

                    <button
                      type="button"
                      className="cancel-button"
                      onClick={closeVoiceAgent}
                    >
                      Close Voice Agent
                    </button>
                  </div>

                  {voiceOutcomeOpen && (
                    <div
                      style={{
                        marginTop: "16px",
                        padding: "16px",
                        borderRadius: "12px",
                        background: "#ffffff",
                        border: "1px solid #dbe3f0",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "12px",
                          fontWeight: "800",
                          letterSpacing: "0.08em",
                          textTransform: "uppercase",
                          opacity: 0.65,
                          marginBottom: "6px",
                        }}
                      >
                        Call Outcome
                      </div>

                      <h4 style={{ margin: "0 0 12px", fontSize: "17px" }}>
                        How did the conversation go?
                      </h4>

                      <select
                        value={voiceOutcomeValue}
                        onChange={(event) =>
                          setVoiceOutcomeValue(event.target.value)
                        }
                        className="crm-filter"
                        style={{ width: "100%", marginBottom: "10px" }}
                        disabled={voiceOutcomeSaving}
                      >
                        <option value="successful">Successful</option>
                        <option value="customer_interested">Customer Interested</option>
                        <option value="customer_declined">Customer Declined</option>
                        <option value="no_response">No Response</option>
                        <option value="rescheduled">Rescheduled</option>
                        <option value="converted">Converted</option>
                        <option value="lost">Lost</option>
                        <option value="pending">Pending</option>
                      </select>

                      <textarea
                        value={voiceOutcomeNotes}
                        onChange={(event) =>
                          setVoiceOutcomeNotes(event.target.value)
                        }
                        placeholder="Add optional notes about the call..."
                        rows={3}
                        style={{
                          width: "100%",
                          boxSizing: "border-box",
                          resize: "vertical",
                          padding: "10px 12px",
                          borderRadius: "8px",
                          border: "1px solid #dbe3f0",
                          fontFamily: "inherit",
                          fontSize: "14px",
                          marginBottom: "10px",
                        }}
                        disabled={voiceOutcomeSaving}
                      />

                      <div
                        style={{
                          display: "flex",
                          gap: "8px",
                          justifyContent: "flex-end",
                          flexWrap: "wrap",
                        }}
                      >
                        <button
                          type="button"
                          className="cancel-button"
                          onClick={() => {
                            setVoiceOutcomeOpen(false);
                            setVoiceAgentStatus("IDLE");
                          }}
                          disabled={voiceOutcomeSaving}
                        >
                          Back to Call
                        </button>
                        <button
                          type="button"
                          className="submit-lead-button"
                          onClick={completeVoiceCall}
                          disabled={voiceOutcomeSaving}
                        >
                          {voiceOutcomeSaving
                            ? "Saving Outcome..."
                            : "Save & End Call"}
                        </button>
                      </div>
                    </div>
                  )}

                  {voiceSession && (
                    <div
                      style={{
                        marginTop: "12px",
                        fontSize: "12px",
                        opacity: 0.6,
                      }}
                    >
                      Session ready · Lead #{voiceSession.lead_id}
                    </div>
                  )}
                </section>
              )}

              {/* ==================================================
                  NEXT BEST ACTION
                  ================================================== */}

              <section
                style={{
                  marginTop: "22px",
                  marginBottom: "22px",
                  padding: "20px 22px",
                  border: "1px solid #dbe3f0",
                  borderRadius: "14px",
                  background: "#f8fbff",
                  boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "16px",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      AI Sales Intelligence
                    </div>

                    <h3
                      style={{
                        margin: 0,
                        fontSize: "20px",
                      }}
                    >
                      Next Best Action
                    </h3>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() => loadNextBestAction(selectedLead.id)}
                    disabled={nextBestActionLoading}
                  >
                    {nextBestActionLoading ? "Loading..." : "Refresh"}
                  </button>
                </div>

                {nextBestActionError && (
                  <div
                    className="error-card"
                    style={{ marginTop: "14px" }}
                  >
                    {nextBestActionError}
                  </div>
                )}

                {nextBestActionLoading ? (
                  <div
                    style={{
                      marginTop: "16px",
                      padding: "14px 0",
                      opacity: 0.7,
                    }}
                  >
                    Determining the next best action...
                  </div>
                ) : nextBestAction ? (
                  <div style={{ marginTop: "16px" }}>
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        padding: "8px 12px",
                        borderRadius: "999px",
                        background: "#e8f1ff",
                        fontWeight: "700",
                        fontSize: "14px",
                        marginBottom: "12px",
                      }}
                    >
                      {String(
                        nextBestAction.action ||
                          "No action available"
                      )
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (letter) =>
                          letter.toUpperCase()
                        )}
                    </div>

                    <p
                      style={{
                        margin: 0,
                        lineHeight: 1.6,
                        opacity: 0.82,
                      }}
                    >
                      {nextBestAction.reason ||
                        "No reason was provided."}
                    </p>
                  </div>
                ) : (
                  <div
                    style={{
                      marginTop: "16px",
                      opacity: 0.7,
                    }}
                  >
                    No next best action is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  LEAD HEALTH & PRIORITY
                  ================================================== */}

              <section
                style={{
                  marginTop: "22px",
                  marginBottom: "22px",
                  padding: "20px 22px",
                  border: "1px solid #dbe3f0",
                  borderRadius: "14px",
                  background: "#ffffff",
                  boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "16px",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      Sales Health
                    </div>

                    <h3
                      style={{
                        margin: 0,
                        fontSize: "20px",
                      }}
                    >
                      Lead Health & Priority
                    </h3>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() => loadLeadHealth(selectedLead.id)}
                    disabled={leadHealthLoading}
                  >
                    {leadHealthLoading ? "Loading..." : "Refresh"}
                  </button>
                </div>

                {leadHealthError && (
                  <div
                    className="error-card"
                    style={{ marginTop: "14px" }}
                  >
                    {leadHealthError}
                  </div>
                )}

                {leadHealthLoading ? (
                  <div
                    style={{
                      marginTop: "16px",
                      padding: "14px 0",
                      opacity: 0.7,
                    }}
                  >
                    Analyzing lead health...
                  </div>
                ) : leadHealth ? (
                  <div style={{ marginTop: "18px" }}>
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "10px",
                        marginBottom: "18px",
                      }}
                    >
                      <span
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          padding: "8px 14px",
                          borderRadius: "999px",
                          background:
                            leadHealth.health === "HOT"
                              ? "#fee2e2"
                              : leadHealth.health === "WARM"
                              ? "#fef3c7"
                              : leadHealth.health === "CONVERTED"
                              ? "#dcfce7"
                              : "#e5e7eb",
                          fontWeight: "800",
                          fontSize: "14px",
                        }}
                      >
                        {leadHealth.health === "HOT"
                          ? "🔥 HOT LEAD"
                          : leadHealth.health === "WARM"
                          ? "🟡 WARM LEAD"
                          : leadHealth.health === "CONVERTED"
                          ? "✅ CONVERTED"
                          : "⚪ COLD LEAD"}
                      </span>

                      <span
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          padding: "8px 14px",
                          borderRadius: "999px",
                          background:
                            leadHealth.priority === "URGENT"
                              ? "#fee2e2"
                              : leadHealth.priority === "HIGH"
                              ? "#ffedd5"
                              : leadHealth.priority === "MEDIUM"
                              ? "#fef3c7"
                              : "#e5e7eb",
                          fontWeight: "800",
                          fontSize: "14px",
                        }}
                      >
                        {leadHealth.priority} PRIORITY
                      </span>
                    </div>

                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(140px, 1fr))",
                        gap: "12px",
                        marginBottom: "18px",
                      }}
                    >
                      <div
                        style={{
                          padding: "12px 14px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "4px",
                          }}
                        >
                          Lead Score
                        </span>
                        <strong style={{ fontSize: "20px" }}>
                          {leadHealth.lead_score ?? 0}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "12px 14px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "4px",
                          }}
                        >
                          Pipeline
                        </span>
                        <strong>
                          {leadHealth.pipeline_stage || "NEW"}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "12px 14px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "4px",
                          }}
                        >
                          Buying Intent
                        </span>
                        <strong style={{ textTransform: "capitalize" }}>
                          {leadHealth.buying_intent || "Unknown"}
                        </strong>
                      </div>
                    </div>

                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#f8fbff",
                        marginBottom: "14px",
                      }}
                    >
                      <strong
                        style={{
                          display: "block",
                          marginBottom: "6px",
                        }}
                      >
                        Recommended Focus
                      </strong>
                      <p
                        style={{
                          margin: 0,
                          lineHeight: 1.6,
                          opacity: 0.82,
                        }}
                      >
                        {leadHealth.recommended_focus ||
                          "No recommendation available."}
                      </p>
                    </div>

                    {leadHealth.risks && leadHealth.risks.length > 0 ? (
                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "10px",
                          background: "#fff7ed",
                          border: "1px solid #fed7aa",
                        }}
                      >
                        <strong
                          style={{
                            display: "block",
                            marginBottom: "8px",
                          }}
                        >
                          ⚠️ Risk Signals
                        </strong>
                        <ul
                          style={{
                            margin: 0,
                            paddingLeft: "20px",
                          }}
                        >
                          {leadHealth.risks.map((risk, index) => (
                            <li key={index}>{risk}</li>
                          ))}
                        </ul>
                      </div>
                    ) : (
                      <div
                        style={{
                          fontSize: "13px",
                          opacity: 0.65,
                        }}
                      >
                        ✓ No current risk signals detected.
                      </div>
                    )}
                  </div>
                ) : (
                  <div
                    style={{
                      marginTop: "16px",
                      opacity: 0.7,
                    }}
                  >
                    No lead health information is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  AI SALES RECOMMENDATION
                  ================================================== */}

              <section
                style={{
                  marginTop: "22px",
                  marginBottom: "22px",
                  padding: "20px 22px",
                  border: "1px solid #dbe3f0",
                  borderRadius: "14px",
                  background: "#f8fbff",
                  boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "16px",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      AI Sales Intelligence
                    </div>

                    <h3
                      style={{
                        margin: 0,
                        fontSize: "20px",
                      }}
                    >
                      Sales Recommendation
                    </h3>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() =>
                      loadSalesRecommendation(selectedLead.id)
                    }
                    disabled={salesRecommendationLoading}
                  >
                    {salesRecommendationLoading ? "Loading..." : "Refresh"}
                  </button>
                </div>

                {salesRecommendationError && (
                  <div
                    className="error-card"
                    style={{ marginTop: "14px" }}
                  >
                    {salesRecommendationError}
                  </div>
                )}

                {salesRecommendationLoading ? (
                  <div
                    style={{
                      marginTop: "16px",
                      padding: "14px 0",
                      opacity: 0.7,
                    }}
                  >
                    Generating sales recommendation...
                  </div>
                ) : salesRecommendation ? (
                  <div style={{ marginTop: "18px" }}>
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "10px",
                        marginBottom: "16px",
                      }}
                    >
                      <span
                        style={{
                          padding: "8px 12px",
                          borderRadius: "999px",
                          background: "#e8f1ff",
                          fontWeight: "700",
                          fontSize: "14px",
                        }}
                      >
                        {String(
                          salesRecommendation.next_best_action ||
                            "review_lead"
                        )
                          .replaceAll("_", " ")
                          .replace(/\b\w/g, (letter) =>
                            letter.toUpperCase()
                          )}
                      </span>

                      <span
                        style={{
                          padding: "8px 12px",
                          borderRadius: "999px",
                          background:
                            salesRecommendation.priority === "URGENT"
                              ? "#fee2e2"
                              : salesRecommendation.priority === "HIGH"
                              ? "#ffedd5"
                              : salesRecommendation.priority === "MEDIUM"
                              ? "#fef3c7"
                              : "#e5e7eb",
                          fontWeight: "700",
                          fontSize: "14px",
                        }}
                      >
                        {salesRecommendation.priority || "LOW"} PRIORITY
                      </span>
                    </div>

                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(180px, 1fr))",
                        gap: "12px",
                        marginBottom: "16px",
                      }}
                    >
                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "10px",
                          background: "#ffffff",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "5px",
                          }}
                        >
                          Recommended Action
                        </span>
                        <strong>
                          {salesRecommendation.recommended_action ||
                            "Review this lead."}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "10px",
                          background: "#ffffff",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "5px",
                          }}
                        >
                          Urgency
                        </span>
                        <strong>
                          {salesRecommendation.urgency ||
                            "Continue normal lead nurturing."}
                        </strong>
                      </div>
                    </div>

                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#ffffff",
                        marginBottom: "14px",
                      }}
                    >
                      <strong
                        style={{
                          display: "block",
                          marginBottom: "6px",
                        }}
                      >
                        Why?
                      </strong>
                      <p
                        style={{
                          margin: 0,
                          lineHeight: 1.6,
                          opacity: 0.82,
                        }}
                      >
                        {salesRecommendation.reason ||
                          "No explanation was provided."}
                      </p>
                    </div>

                    {/* ==================================================
                        AI LEARNING EVIDENCE
                        ================================================== */}
                    {salesRecommendation.learning && (
                      <div
                        style={{
                          marginBottom: "14px",
                          padding: "16px",
                          borderRadius: "10px",
                          background: "#f5f3ff",
                          border: "1px solid #ddd6fe",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "flex-start",
                            gap: "12px",
                            flexWrap: "wrap",
                            marginBottom: "12px",
                          }}
                        >
                          <div>
                            <strong
                              style={{
                                display: "block",
                                marginBottom: "4px",
                              }}
                            >
                              🧠 AI Learning Evidence
                            </strong>
                            <span
                              style={{
                                fontSize: "12px",
                                opacity: 0.7,
                              }}
                            >
                              Historical outcomes are informing this recommendation.
                            </span>
                          </div>

                          <span
                            style={{
                              padding: "6px 10px",
                              borderRadius: "999px",
                              background:
                                salesRecommendation.learning.confidence === "HIGH"
                                  ? "#dcfce7"
                                  : salesRecommendation.learning.confidence === "MEDIUM"
                                  ? "#fef3c7"
                                  : salesRecommendation.learning.confidence === "LOW"
                                  ? "#e0e7ff"
                                  : "#e5e7eb",
                              fontSize: "11px",
                              fontWeight: "800",
                            }}
                          >
                            {salesRecommendation.learning.confidence || "UNKNOWN"} CONFIDENCE
                          </span>
                        </div>

                        <div
                          style={{
                            display: "grid",
                            gridTemplateColumns:
                              "repeat(auto-fit, minmax(150px, 1fr))",
                            gap: "10px",
                            marginBottom: "12px",
                          }}
                        >
                          <div
                            style={{
                              padding: "11px 12px",
                              borderRadius: "8px",
                              background: "#ffffff",
                            }}
                          >
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.6, marginBottom: "4px" }}>
                              Historical Positive Rate
                            </span>
                            <strong>
                              {salesRecommendation.learning.positive_rate == null
                                ? "No history"
                                : `${salesRecommendation.learning.positive_rate}%`}
                            </strong>
                          </div>

                          <div
                            style={{
                              padding: "11px 12px",
                              borderRadius: "8px",
                              background: "#ffffff",
                            }}
                          >
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.6, marginBottom: "4px" }}>
                              Decided Outcomes
                            </span>
                            <strong>
                              {salesRecommendation.learning.sample_size ?? 0}
                            </strong>
                          </div>

                          <div
                            style={{
                              padding: "11px 12px",
                              borderRadius: "8px",
                              background: "#ffffff",
                            }}
                          >
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.6, marginBottom: "4px" }}>
                              Learning Score
                            </span>
                            <strong>
                              {salesRecommendation.learning.learning_score ?? "—"}
                            </strong>
                          </div>
                        </div>

                        <p
                          style={{
                            margin: 0,
                            fontSize: "13px",
                            lineHeight: 1.55,
                            opacity: 0.82,
                          }}
                        >
                          {salesRecommendation.learning_context ||
                            "No additional learning context is available."}
                        </p>
                      </div>
                    )}

                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#ffffff",
                      }}
                    >
                      <strong
                        style={{
                          display: "block",
                          marginBottom: "8px",
                        }}
                      >
                        Suggested Message
                      </strong>

                      <p
                        style={{
                          margin: 0,
                          lineHeight: 1.6,
                          opacity: 0.85,
                        }}
                      >
                        {salesRecommendation.suggested_message ||
                          "No suggested message available."}
                      </p>
                    </div>

                    {salesRecommendation.learning && (
                      <div
                        style={{
                          marginTop: "14px",
                          padding: "16px",
                          borderRadius: "12px",
                          background: "#f7f5ff",
                          border: "1px solid #e4ddff",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "flex-start",
                            gap: "12px",
                            flexWrap: "wrap",
                            marginBottom: "12px",
                          }}
                        >
                          <div>
                            <strong
                              style={{
                                display: "block",
                                marginBottom: "4px",
                                fontSize: "15px",
                              }}
                            >
                              🧠 AI Learning Evidence
                            </strong>
                            <span style={{ fontSize: "12px", opacity: 0.7 }}>
                              Historical outcomes are informing this recommendation.
                            </span>
                          </div>

                          <span
                            style={{
                              padding: "6px 10px",
                              borderRadius: "999px",
                              background:
                                String(
                                  salesRecommendation.learning.confidence || ""
                                ).toUpperCase() === "HIGH"
                                  ? "#dcfce7"
                                  : String(
                                      salesRecommendation.learning.confidence || ""
                                    ).toUpperCase() === "MEDIUM"
                                  ? "#fef3c7"
                                  : "#ede9fe",
                              fontSize: "11px",
                              fontWeight: "800",
                            }}
                          >
                            {String(
                              salesRecommendation.learning.confidence || "UNKNOWN"
                            ).toUpperCase()} CONFIDENCE
                          </span>
                        </div>

                        <div
                          style={{
                            display: "grid",
                            gridTemplateColumns:
                              "repeat(auto-fit, minmax(130px, 1fr))",
                            gap: "10px",
                            marginBottom: "12px",
                          }}
                        >
                          <div style={{ padding: "11px 12px", borderRadius: "9px", background: "#fff" }}>
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.65, marginBottom: "4px" }}>
                              Historical Positive Rate
                            </span>
                            <strong>{salesRecommendation.learning.positive_rate ?? 0}%</strong>
                          </div>

                          <div style={{ padding: "11px 12px", borderRadius: "9px", background: "#fff" }}>
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.65, marginBottom: "4px" }}>
                              Decided Outcomes
                            </span>
                            <strong>{salesRecommendation.learning.sample_size ?? 0}</strong>
                          </div>

                          <div style={{ padding: "11px 12px", borderRadius: "9px", background: "#fff" }}>
                            <span style={{ display: "block", fontSize: "11px", opacity: 0.65, marginBottom: "4px" }}>
                              Learning Score
                            </span>
                            <strong>{salesRecommendation.learning.learning_score ?? 0}</strong>
                          </div>

                          {salesRecommendation.adaptive_action && (
                            <div style={{ padding: "11px 12px", borderRadius: "9px", background: "#fff" }}>
                              <span style={{ display: "block", fontSize: "11px", opacity: 0.65, marginBottom: "4px" }}>
                                Adaptive Score
                              </span>
                              <strong>
                                {salesRecommendation.adaptive_action.adaptive_score ?? 0}
                              </strong>
                            </div>
                          )}
                        </div>

                        {salesRecommendation.adaptive_action && (
                          <div
                            style={{
                              display: "flex",
                              flexWrap: "wrap",
                              gap: "8px",
                              marginBottom: "12px",
                              fontSize: "12px",
                            }}
                          >
                            <span style={{ padding: "6px 9px", borderRadius: "8px", background: "#fff" }}>
                              Base score: <strong>{salesRecommendation.adaptive_action.base_score ?? 0}</strong>
                            </span>
                            <span style={{ padding: "6px 9px", borderRadius: "8px", background: "#fff" }}>
                              Learning adjustment:{" "}
                              <strong>{salesRecommendation.adaptive_action.learning_adjustment ?? 0}</strong>
                            </span>
                          </div>
                        )}

                        <p
                          style={{
                            margin: 0,
                            fontSize: "13px",
                            lineHeight: 1.55,
                            opacity: 0.78,
                          }}
                        >
                          {salesRecommendation.learning_context ||
                            `Historical outcomes for '${formatAction(
                              salesRecommendation.learning.action
                            )}' are informing this recommendation.`}
                        </p>
                      </div>
                    )}

                    {/* ==================================================
                        EXECUTE RECOMMENDED ACTION
                  ================================================== */}
                    <div
                      style={{
                        marginTop: "14px",
                        padding: "16px",
                        borderRadius: "10px",
                        background: "#f8fafc",
                        border: "1px solid #e5e7eb",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          gap: "12px",
                          flexWrap: "wrap",
                        }}
                      >
                        <div>
                          <strong style={{ display: "block", marginBottom: "4px" }}>
                            Execute Next Action
                          </strong>
                          <span style={{ fontSize: "13px", opacity: 0.7 }}>
                            Apply this recommendation to the CRM.
                          </span>
                        </div>

                        <button
                          type="button"
                          className="submit-lead-button"
                          onClick={() =>
                            handleExecuteSalesAction(
                              salesRecommendation.next_best_action
                            )
                          }
                          disabled={
                            executingSalesAction ||
                            !salesRecommendation.next_best_action
                          }
                        >
                          {executingSalesAction
                            ? "Executing..."
                            : salesRecommendation.next_best_action ===
                              "contact_and_reschedule_site_visit"
                            ? "Contact & Reschedule Site Visit"
                            : salesRecommendation.next_best_action ===
                              "prepare_for_site_visit"
                            ? "Prepare for Site Visit"
                            : salesRecommendation.next_best_action ===
                              "follow_up_after_site_visit"
                            ? "Follow Up After Site Visit"
                            : salesRecommendation.next_best_action ===
                              "schedule_site_visit"
                            ? "Schedule Site Visit"
                            : salesRecommendation.next_best_action ===
                              "recommend_properties"
                            ? "Recommend Properties"
                            : salesRecommendation.next_best_action ===
                              "discuss_negotiation"
                            ? "Discuss Negotiation"
                            : salesRecommendation.next_best_action ===
                              "contact_high_intent_lead"
                            ? "Contact High-Intent Lead"
                            : salesRecommendation.next_best_action ===
                              "qualify_lead"
                            ? "Qualify Lead"
                            : salesRecommendation.next_best_action ===
                              "follow_up_on_pending_task"
                            ? "Complete Pending Follow-up"
                            : "Execute Action"}
                        </button>
                      </div>

                      {salesActionSuccess && (
                        <div
                          className="form-success"
                          style={{ marginTop: "12px" }}
                        >
                          {salesActionSuccess}
                        </div>
                      )}

                      {salesActionError && (
                        <div
                          className="form-error"
                          style={{ marginTop: "12px" }}
                        >
                          {salesActionError}
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div
                    style={{
                      marginTop: "16px",
                      opacity: 0.7,
                    }}
                  >
                    No sales recommendation is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  FOLLOW-UP INTELLIGENCE
                  ================================================== */}

              <section
                style={{
                  marginTop: "22px",
                  marginBottom: "22px",
                  padding: "20px 22px",
                  border: "1px solid #dbe3f0",
                  borderRadius: "14px",
                  background: "#ffffff",
                  boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "16px",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: "700",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "6px",
                        opacity: 0.65,
                      }}
                    >
                      AI Sales Intelligence
                    </div>

                    <h3
                      style={{
                        margin: 0,
                        fontSize: "20px",
                      }}
                    >
                      Follow-Up Intelligence
                    </h3>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() =>
                      loadFollowUpIntelligence(selectedLead.id)
                    }
                    disabled={followUpIntelligenceLoading}
                  >
                    {followUpIntelligenceLoading ? "Loading..." : "Refresh"}
                  </button>
                </div>

                {followUpIntelligenceError && (
                  <div
                    className="error-card"
                    style={{ marginTop: "14px" }}
                  >
                    {followUpIntelligenceError}
                  </div>
                )}

                {followUpIntelligenceLoading ? (
                  <div
                    style={{
                      marginTop: "16px",
                      padding: "14px 0",
                      opacity: 0.7,
                    }}
                  >
                    Analyzing the best follow-up timing...
                  </div>
                ) : followUpIntelligence ? (
                  <div style={{ marginTop: "18px" }}>
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "10px",
                        marginBottom: "16px",
                      }}
                    >
                      <span
                        style={{
                          padding: "8px 12px",
                          borderRadius: "999px",
                          background:
                            followUpIntelligence.follow_up_status === "ACT_NOW"
                              ? "#fee2e2"
                              : followUpIntelligence.follow_up_status === "FOLLOW_UP"
                              ? "#fef3c7"
                              : "#dcfce7",
                          color:
                            followUpIntelligence.follow_up_status === "ACT_NOW"
                              ? "#b91c1c"
                              : followUpIntelligence.follow_up_status === "FOLLOW_UP"
                              ? "#92400e"
                              : "#166534",
                          fontWeight: "800",
                          fontSize: "13px",
                        }}
                      >
                        {followUpIntelligence.follow_up_status === "ACT_NOW"
                          ? "🔴 ACT NOW"
                          : followUpIntelligence.follow_up_status === "FOLLOW_UP"
                          ? "🟡 FOLLOW UP"
                          : "🟢 WAIT"}
                      </span>

                      <span
                        style={{
                          padding: "8px 12px",
                          borderRadius: "999px",
                          background: "#f1f5f9",
                          fontWeight: "700",
                          fontSize: "13px",
                        }}
                      >
                        {followUpIntelligence.priority || "LOW"} PRIORITY
                      </span>
                    </div>

                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(180px, 1fr))",
                        gap: "12px",
                        marginBottom: "14px",
                      }}
                    >
                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "5px",
                          }}
                        >
                          Recommended Timing
                        </span>
                        <strong>
                          {String(
                            followUpIntelligence.recommended_timing ||
                              "monitor"
                          )
                            .replaceAll("_", " ")
                            .replace(/\b\w/g, (letter) =>
                              letter.toUpperCase()
                            )}
                        </strong>
                      </div>

                      <div
                        style={{
                          padding: "14px 16px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                        }}
                      >
                        <span
                          style={{
                            display: "block",
                            fontSize: "12px",
                            opacity: 0.65,
                            marginBottom: "5px",
                          }}
                        >
                          Objective
                        </span>
                        <strong>
                          {followUpIntelligence.objective ||
                            "Continue normal lead nurturing."}
                        </strong>
                      </div>
                    </div>

                    <div
                      style={{
                        padding: "14px 16px",
                        borderRadius: "10px",
                        background: "#f8fafc",
                      }}
                    >
                      <strong
                        style={{
                          display: "block",
                          marginBottom: "6px",
                        }}
                      >
                        Why now?
                      </strong>
                      <p
                        style={{
                          margin: 0,
                          lineHeight: 1.6,
                          opacity: 0.82,
                        }}
                      >
                        {followUpIntelligence.reason ||
                          "No immediate follow-up trigger was detected."}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div
                    style={{
                      marginTop: "16px",
                      opacity: 0.7,
                    }}
                  >
                    No follow-up intelligence is currently available.
                  </div>
                )}
              </section>


              {/* ==================================================
                  AI SALES HISTORY & ACTION OUTCOMES
                  ================================================== */}

              {salesRecommendation && (
                <section
                  style={{
                    marginTop: "22px",
                    marginBottom: "22px",
                    padding: "20px 22px",
                    border: "1px solid #dbe3f0",
                    borderRadius: "14px",
                    background: "#f8fbff",
                    boxShadow: "0 4px 14px rgba(15, 23, 42, 0.05)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      gap: "16px",
                      flexWrap: "wrap",
                    }}
                  >
                    <div>
                      <div
                        style={{
                          fontSize: "12px",
                          fontWeight: "700",
                          letterSpacing: "0.08em",
                          textTransform: "uppercase",
                          opacity: 0.65,
                          marginBottom: "5px",
                        }}
                      >
                        AI Context
                      </div>
                      <h3 style={{ margin: 0, fontSize: "20px" }}>
                        Sales History & Outcomes
                      </h3>
                      <p style={{ margin: "6px 0 0", opacity: 0.7 }}>
                        Recent sales activity and the outcomes of AI-recommended actions.
                      </p>
                    </div>

                    <span
                      style={{
                        padding: "7px 11px",
                        borderRadius: "999px",
                        background: "#e8f1ff",
                        fontSize: "12px",
                        fontWeight: "700",
                      }}
                    >
                      {salesRecommendation.sales_history?.event_count ??
                        salesRecommendation.sales_history?.events?.length ??
                        0} events
                    </span>
                  </div>

                  {salesRecommendation.sales_history ? (
                    <>
                      {salesRecommendation.sales_history.insights?.length > 0 && (
                        <div
                          style={{
                            marginTop: "16px",
                            padding: "14px 16px",
                            borderRadius: "10px",
                            background: "#ffffff",
                            border: "1px solid #eef2f7",
                          }}
                        >
                          <strong style={{ display: "block", marginBottom: "7px" }}>
                            AI-Relevant Signals
                          </strong>
                          <ul
                            style={{
                              margin: 0,
                              paddingLeft: "20px",
                              lineHeight: 1.7,
                            }}
                          >
                            {salesRecommendation.sales_history.insights.map(
                              (insight, index) => (
                                <li key={`${index}-${insight}`}>{insight}</li>
                              )
                            )}
                          </ul>
                        </div>
                      )}
                    </>
                  ) : (
                    <div
                      style={{
                        marginTop: "16px",
                        padding: "12px 14px",
                        background: "#ffffff",
                        borderRadius: "10px",
                        opacity: 0.7,
                      }}
                    >
                      No sales history is included in the current API response.
                    </div>
                  )}

                  {/* ==================================================
                      ACTION OUTCOMES
                  ================================================== */}
                  {(() => {
                    const actionOutcomes = Array.isArray(
                      salesRecommendation.sales_history?.action_outcomes
                    )
                      ? salesRecommendation.sales_history.action_outcomes
                      : [];

                    const latestOutcome =
                      salesRecommendation.sales_history?.latest_action_outcome ||
                      actionOutcomes[0] ||
                      null;

                    const formatAction = (action) =>
                      String(action || "Sales Action")
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (letter) => letter.toUpperCase());

                    const formatOutcome = (outcome) =>
                      String(outcome || "PENDING")
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (letter) => letter.toUpperCase());

                    const outcomeValue = (item) =>
                      item?.outcome ||
                      item?.status ||
                      item?.result ||
                      "PENDING";

                    const outcomeIsPositive = (item) =>
                      [
                        "completed",
                        "converted",
                        "rescheduled",
                        "scheduled",
                        "contacted",
                        "qualified",
                        "success",
                      ].includes(String(outcomeValue(item)).toLowerCase());

                    return (
                      <div style={{ marginTop: "16px" }}>
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            gap: "12px",
                            marginBottom: "10px",
                            flexWrap: "wrap",
                          }}
                        >
                          <div>
                            <strong style={{ fontSize: "16px" }}>
                              AI Action Outcomes
                            </strong>
                            <div
                              style={{
                                marginTop: "3px",
                                fontSize: "12px",
                                opacity: 0.65,
                              }}
                            >
                              What happened after recommended sales actions were executed.
                            </div>
                          </div>
                          <span
                            style={{
                              fontSize: "12px",
                              fontWeight: "700",
                              opacity: 0.7,
                            }}
                          >
                            {actionOutcomes.length} tracked
                          </span>
                        </div>

                        {latestOutcome && (
                          <div
                            style={{
                              padding: "15px 16px",
                              borderRadius: "10px",
                              background: "#ffffff",
                              border: "1px solid #dbe3f0",
                              marginBottom: "12px",
                            }}
                          >
                            <div
                              style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "flex-start",
                                gap: "12px",
                                flexWrap: "wrap",
                              }}
                            >
                              <div>
                                <span
                                  style={{
                                    display: "block",
                                    fontSize: "11px",
                                    fontWeight: "700",
                                    textTransform: "uppercase",
                                    letterSpacing: "0.06em",
                                    opacity: 0.6,
                                    marginBottom: "4px",
                                  }}
                                >
                                  Latest Sales Action
                                </span>
                                <strong style={{ fontSize: "16px" }}>
                                  {formatAction(
                                    latestOutcome.action ||
                                      latestOutcome.next_best_action ||
                                      salesRecommendation.next_best_action
                                  )}
                                </strong>
                              </div>

                              <span
                                style={{
                                  padding: "6px 10px",
                                  borderRadius: "999px",
                                  background: outcomeIsPositive(latestOutcome)
                                    ? "#dcfce7"
                                    : String(outcomeValue(latestOutcome)).toLowerCase() ===
                                      "pending"
                                    ? "#fef3c7"
                                    : "#fee2e2",
                                  fontSize: "12px",
                                  fontWeight: "800",
                                }}
                              >
                                {formatOutcome(outcomeValue(latestOutcome))}
                              </span>
                            </div>

                            <div
                              style={{
                                display: "grid",
                                gridTemplateColumns:
                                  "repeat(auto-fit, minmax(160px, 1fr))",
                                gap: "10px",
                                marginTop: "13px",
                              }}
                            >
                              <div
                                style={{
                                  padding: "10px 12px",
                                  borderRadius: "8px",
                                  background: "#f8fafc",
                                }}
                              >
                                <span
                                  style={{
                                    display: "block",
                                    fontSize: "11px",
                                    opacity: 0.6,
                                    marginBottom: "3px",
                                  }}
                                >
                                  Execution
                                </span>
                                <strong>
                                  {formatOutcome(
                                    latestOutcome.execution_status ||
                                      latestOutcome.status ||
                                      "executed"
                                  )}
                                </strong>
                              </div>

                              <div
                                style={{
                                  padding: "10px 12px",
                                  borderRadius: "8px",
                                  background: "#f8fafc",
                                }}
                              >
                                <span
                                  style={{
                                    display: "block",
                                    fontSize: "11px",
                                    opacity: 0.6,
                                    marginBottom: "3px",
                                  }}
                                >
                                  Outcome
                                </span>
                                <strong>{formatOutcome(outcomeValue(latestOutcome))}</strong>
                              </div>

                              {latestOutcome.date && (
                                <div
                                  style={{
                                    padding: "10px 12px",
                                    borderRadius: "8px",
                                    background: "#f8fafc",
                                  }}
                                >
                                  <span
                                    style={{
                                      display: "block",
                                      fontSize: "11px",
                                      opacity: 0.6,
                                      marginBottom: "3px",
                                    }}
                                  >
                                    Date
                                  </span>
                                  <strong>{formatDate(latestOutcome.date)}</strong>
                                </div>
                              )}
                            </div>

                            {(latestOutcome.notes ||
                              latestOutcome.message ||
                              latestOutcome.reason ||
                              latestOutcome.description) && (
                              <p
                                style={{
                                  margin: "12px 0 0",
                                  fontSize: "13px",
                                  lineHeight: 1.55,
                                  opacity: 0.78,
                                }}
                              >
                                {latestOutcome.notes ||
                                  latestOutcome.message ||
                                  latestOutcome.reason ||
                                  latestOutcome.description}
                              </p>
                            )}

                            {String(outcomeValue(latestOutcome)).toLowerCase() ===
                              "pending" && (
                              <div
                                style={{
                                  marginTop: "10px",
                                  fontSize: "12px",
                                  fontWeight: "600",
                                  opacity: 0.7,
                                }}
                              >
                                ⏳ Awaiting the real-world sales outcome.
                              </div>
                            )}
                          </div>
                        )}

                        {latestOutcome &&
                          String(outcomeValue(latestOutcome)).toLowerCase() ===
                            "pending" && (
                            <div
                              style={{
                                marginBottom: "12px",
                                padding: "14px 15px",
                                borderRadius: "10px",
                                background: "#fffdf5",
                                border: "1px solid #f3df9b",
                              }}
                            >
                              {!outcomeFormOpen ? (
                                <div
                                  style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    gap: "12px",
                                    flexWrap: "wrap",
                                  }}
                                >
                                  <div>
                                    <strong style={{ display: "block" }}>
                                      Outcome required
                                    </strong>
                                    <span
                                      style={{
                                        display: "block",
                                        marginTop: "3px",
                                        fontSize: "12px",
                                        opacity: 0.7,
                                      }}
                                    >
                                      Record what happened after this AI sales action.
                                    </span>
                                  </div>

                                  <button
                                    type="button"
                                    onClick={() => setOutcomeFormOpen(true)}
                                    style={{
                                      padding: "9px 13px",
                                      border: "none",
                                      borderRadius: "8px",
                                      background: "#2563eb",
                                      color: "#ffffff",
                                      fontWeight: "700",
                                      cursor: "pointer",
                                    }}
                                  >
                                    Record Outcome
                                  </button>
                                </div>
                              ) : (
                                <div>
                                  <strong
                                    style={{
                                      display: "block",
                                      marginBottom: "9px",
                                    }}
                                  >
                                    Record Sales Outcome
                                  </strong>

                                  <select
                                    value={outcomeValueInput}
                                    onChange={(event) =>
                                      setOutcomeValueInput(event.target.value)
                                    }
                                    style={{
                                      width: "100%",
                                      boxSizing: "border-box",
                                      padding: "9px 10px",
                                      borderRadius: "7px",
                                      border: "1px solid #d1d5db",
                                      background: "#ffffff",
                                      marginBottom: "9px",
                                    }}
                                  >
                                    <option value="successful">
                                      Successful
                                    </option>
                                    <option value="customer_interested">
                                      Customer Interested
                                    </option>
                                    <option value="customer_declined">
                                      Customer Declined
                                    </option>
                                    <option value="no_response">
                                      No Response
                                    </option>
                                    <option value="rescheduled">
                                      Rescheduled
                                    </option>
                                    <option value="converted">
                                      Converted
                                    </option>
                                    <option value="lost">
                                      Lost
                                    </option>
                                  </select>

                                  <textarea
                                    value={outcomeNotes}
                                    onChange={(event) =>
                                      setOutcomeNotes(event.target.value)
                                    }
                                    rows={3}
                                    placeholder="Add a short note about what happened..."
                                    style={{
                                      width: "100%",
                                      boxSizing: "border-box",
                                      padding: "9px 10px",
                                      borderRadius: "7px",
                                      border: "1px solid #d1d5db",
                                      resize: "vertical",
                                      marginBottom: "9px",
                                      fontFamily: "inherit",
                                    }}
                                  />

                                  <div
                                    style={{
                                      display: "flex",
                                      justifyContent: "flex-end",
                                      gap: "8px",
                                    }}
                                  >
                                    <button
                                      type="button"
                                      onClick={() => {
                                        setOutcomeFormOpen(false);
                                        setOutcomeNotes("");
                                        setOutcomeValueInput("successful");
                                      }}
                                      disabled={savingOutcome}
                                      style={{
                                        padding: "8px 12px",
                                        borderRadius: "7px",
                                        border: "1px solid #d1d5db",
                                        background: "#ffffff",
                                        cursor: savingOutcome
                                          ? "not-allowed"
                                          : "pointer",
                                      }}
                                    >
                                      Cancel
                                    </button>

                                    <button
                                      type="button"
                                      onClick={handleRecordSalesActionOutcome}
                                      disabled={savingOutcome}
                                      style={{
                                        padding: "8px 13px",
                                        borderRadius: "7px",
                                        border: "none",
                                        background: "#2563eb",
                                        color: "#ffffff",
                                        fontWeight: "700",
                                        cursor: savingOutcome
                                          ? "wait"
                                          : "pointer",
                                      }}
                                    >
                                      {savingOutcome
                                        ? "Saving..."
                                        : "Save Outcome"}
                                    </button>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}

                        {actionOutcomes.length > 0 ? (
                          <div
                            style={{
                              display: "grid",
                              gap: "8px",
                            }}
                          >
                            {actionOutcomes.slice(0, 8).map((item, index) => {
                              const outcome = outcomeValue(item);
                              const positive = outcomeIsPositive(item);

                              return (
                                <div
                                  key={`${item.id || item.action || index}-${item.date || ""}`}
                                  style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    gap: "12px",
                                    padding: "11px 13px",
                                    borderRadius: "9px",
                                    background: "#ffffff",
                                    border: "1px solid #eef2f7",
                                  }}
                                >
                                  <div style={{ minWidth: 0 }}>
                                    <strong style={{ display: "block" }}>
                                      {formatAction(
                                        item.action ||
                                          item.next_best_action ||
                                          item.type
                                      )}
                                    </strong>
                                    <span
                                      style={{
                                        display: "block",
                                        marginTop: "3px",
                                        fontSize: "12px",
                                        opacity: 0.6,
                                      }}
                                    >
                                      {item.date
                                        ? formatDate(item.date)
                                        : item.created_at
                                        ? formatDate(item.created_at)
                                        : "Recent action"}
                                    </span>
                                  </div>

                                  <span
                                    style={{
                                      flexShrink: 0,
                                      padding: "5px 9px",
                                      borderRadius: "999px",
                                      background: positive
                                        ? "#dcfce7"
                                        : String(outcome).toLowerCase() === "pending"
                                        ? "#fef3c7"
                                        : "#fee2e2",
                                      fontSize: "11px",
                                      fontWeight: "800",
                                    }}
                                  >
                                    {formatOutcome(outcome)}
                                  </span>
                                </div>
                              );
                            })}
                          </div>
                        ) : (
                          <div
                            style={{
                              padding: "12px 14px",
                              borderRadius: "9px",
                              background: "#ffffff",
                              border: "1px solid #eef2f7",
                              fontSize: "13px",
                              opacity: 0.7,
                            }}
                          >
                            No executed AI sales actions have outcomes recorded yet.
                          </div>
                        )}
                      </div>
                    );
                  })()}

                  {/* ==================================================
                      RECENT SALES EVENTS
                  ================================================== */}
                  {salesRecommendation.sales_history?.events?.length > 0 ? (
                    <div style={{ marginTop: "18px" }}>
                      <div style={{ marginBottom: "9px" }}>
                        <strong style={{ fontSize: "16px" }}>Recent Events</strong>
                      </div>

                      <div
                        style={{
                          display: "grid",
                          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                          gap: "9px",
                        }}
                      >
                        {salesRecommendation.sales_history.events
                          .slice(0, 8)
                          .map((event, index) => (
                            <div
                              key={`${event.type || "event"}-${event.id || index}-${event.date || ""}`}
                              style={{
                                padding: "12px 13px",
                                borderRadius: "9px",
                                background: "#ffffff",
                                border: "1px solid #eef2f7",
                              }}
                            >
                              <div
                                style={{
                                  display: "flex",
                                  justifyContent: "space-between",
                                  gap: "8px",
                                  marginBottom: "4px",
                                }}
                              >
                                <strong>
                                  {String(event.type || "event")
                                    .replaceAll("_", " ")
                                    .replace(/\b\w/g, (letter) => letter.toUpperCase())}
                                </strong>
                                {event.status && (
                                  <span
                                    style={{
                                      fontSize: "10px",
                                      fontWeight: "700",
                                      textTransform: "uppercase",
                                      opacity: 0.6,
                                    }}
                                  >
                                    {event.status}
                                  </span>
                                )}
                              </div>

                              {event.date && (
                                <div
                                  style={{
                                    fontSize: "11px",
                                    opacity: 0.6,
                                    marginBottom: "4px",
                                  }}
                                >
                                  {formatDate(event.date)}
                                </div>
                              )}

                              {(event.message || event.description || event.notes) && (
                                <div
                                  style={{
                                    fontSize: "12px",
                                    lineHeight: 1.5,
                                    opacity: 0.78,
                                  }}
                                >
                                  {event.message || event.description || event.notes}
                                </div>
                              )}
                            </div>
                          ))}
                      </div>
                    </div>
                  ) : null}
                </section>
              )}

                  {/* ==================================================
                  REQUIREMENT
                      ================================================== */}

              <div className="requirement-section">

                <span>
                  Original Requirement
                </span>

                <p>
                  {selectedLead.requirement ||
                    "No requirement provided."}
                </p>

              </div>


              {/* ==================================================
                  AI CHAT
                  ================================================== */}

              <section className="conversation-section">

                <div className="conversation-section-header">

                  <div>
                    <h3>
                      AI Sales Agent
                    </h3>

                    <p>
                      Continue the conversation with
                      this lead's AI assistant.
                    </p>
                  </div>

                </div>


                {leadDetailsLoading ? (

                  <div className="conversation-loading">
                    Loading conversation...
                  </div>

                ) : (

                  <>

                    {chatError && (
                      <div className="conversation-error">
                        {chatError}
                      </div>
                    )}


                    <div className="conversation-list">

                      {conversations.length === 0 ? (

                        <div className="conversation-empty">
                          No conversation yet.
                          Send the first message below.
                        </div>

                      ) : (

                        conversations.map(
                          (conversation, index) => (

                            <div
                              key={
                                `${conversation.created_at}-${index}`
                              }
                              className={`conversation-message ${
                                conversation.role ===
                                "user"
                                  ? "customer-message"
                                  : "assistant-message"
                              }`}
                            >

                              <div className="conversation-role">
                                {conversation.role ===
                                "user"
                                  ? "YOU"
                                  : "AI SALES AGENT"}
                              </div>

                              <div className="conversation-text">
                                {conversation.message}
                              </div>

                              {conversation.created_at && (
                                <div className="conversation-time">
                                  {formatDate(
                                    conversation.created_at
                                  )}
                                </div>
                              )}

                            </div>

                          )
                        )

                      )}

                    </div>


                    <form
                      className="chat-form"
                      onSubmit={handleSendMessage}
                    >

                      <textarea
                        className="chat-input"
                        value={chatMessage}
                        onChange={(event) =>
                          setChatMessage(
                            event.target.value
                          )
                        }
                        placeholder="Ask the AI about this lead..."
                        rows={3}
                        disabled={sendingMessage}
                      />

                      <button
                        type="submit"
                        className="chat-send-button"
                        disabled={
                          sendingMessage ||
                          !chatMessage.trim()
                        }
                      >
                        {sendingMessage
                          ? "Thinking..."
                          : "Send Message"}
                      </button>

                    </form>

                  </>

                )}

              </section>


              {/* ==================================================
                  ACTIVITY TIMELINE
                  ================================================== */}

              <section className="lead-activity-section">

                <div className="lead-activity-header">
                  <div>
                    <h3>Activity Timeline</h3>
                    <p>
                      Complete history of actions and communications for this lead.
                    </p>
                  </div>

                  <button
                    type="button"
                    className="refresh-button"
                    onClick={() => loadLeadActivities(selectedLead.id)}
                    disabled={leadActivitiesLoading}
                  >
                    {leadActivitiesLoading ? "Loading..." : "Refresh"}
                  </button>
                </div>

                {leadActivitiesError && (
                  <div className="activity-timeline-error">
                    {leadActivitiesError}
                  </div>
                )}

                {leadActivitiesLoading ? (
                  <div className="activity-timeline-empty">
                    Loading activity timeline...
                  </div>
                ) : leadActivities.length === 0 ? (
                  <div className="activity-timeline-empty">
                    No activity recorded for this lead yet.
                  </div>
                ) : (
                  <div className="activity-timeline">

                    {leadActivities.map((activity, index) => (
                      <div
                        className="timeline-item"
                        key={`${activity.type}-${activity.date}-${index}`}
                      >

                        <div className="timeline-marker">
                          {activityIcon(activity.type)}
                        </div>

                        <div className="timeline-content">

                          <div className="timeline-top">
                            <div>
                              <span className="timeline-type">
                                {activityLabel(activity.type)}
                              </span>

                              <h4>
                                {activity.title || activityLabel(activity.type)}
                              </h4>
                            </div>

                            <span
                              className={`timeline-status ${
                                String(activity.status || "")
                                  .toLowerCase()
                                  .replaceAll(" ", "-")
                              }`}
                            >
                              {activity.status || "unknown"}
                            </span>
                          </div>

                          <p className="timeline-description">
                            {activity.description || "No description available."}
                          </p>

                          <div className="timeline-date">
                            {formatDate(activity.date)}
                          </div>

                          {activity.metadata &&
                            Object.keys(activity.metadata).length > 0 && (
                              <div className="timeline-metadata">
                                {activity.metadata.channel && (
                                  <span>
                                    Channel: {activity.metadata.channel}
                                  </span>
                                )}

                                {activity.metadata.direction && (
                                  <span>
                                    Direction: {activity.metadata.direction}
                                  </span>
                                )}

                                {activity.metadata.follow_up_id && (
                                  <span>
                                    Follow-up #{activity.metadata.follow_up_id}
                                  </span>
                                )}

                                {activity.metadata.site_visit_id && (
                                  <span>
                                    Site Visit #{activity.metadata.site_visit_id}
                                  </span>
                                )}

                                {activity.metadata.property_title && (
                                  <span>
                                    Property: {activity.metadata.property_title}
                                  </span>
                                )}
                              </div>
                            )}

                        </div>
                      </div>
                    ))}

                  </div>
                )}

              </section>

            </div>

          </div>

        </div>

      )}


      {/* ======================================================
          FOLLOW-UP MODAL
                  ================================================== */}

      {showFollowUp && selectedLead && (

        <div
          className="modal-overlay follow-up-modal-overlay"
          onMouseDown={(event) => {

            if (
              event.target === event.currentTarget &&
              !schedulingFollowUp
            ) {
              setShowFollowUp(false);
            }

          }}
        >

          <div className="modal follow-up-modal">

            <div className="modal-header">

              <div>

                <h2>
                  Schedule Follow-up
                </h2>

                <p>
                  Schedule a follow-up for{" "}
                  {selectedLead.name ||
                    "this lead"}.
                </p>

              </div>

              <button
                className="close-button"
                onClick={() =>
                  setShowFollowUp(false)
                }
                disabled={schedulingFollowUp}
              >
                Ã—
              </button>

            </div>


            <form
              className="lead-form"
              onSubmit={handleScheduleFollowUp}
            >

              {followUpError && (
                <div className="form-error">
                  {followUpError}
                </div>
              )}

              {followUpSuccess && (
                <div className="form-success">
                  {followUpSuccess}
                </div>
              )}


              <div className="form-group">

                <label>
                  Follow-up Date & Time
                </label>

                <input
                  type="datetime-local"
                  value={
                    followUpForm.follow_up_date
                  }
                  onChange={(event) =>
                    setFollowUpForm({
                      ...followUpForm,
                      follow_up_date:
                        event.target.value,
                    })
                  }
                  disabled={schedulingFollowUp}
                />

              </div>


              <div className="form-group">

                <label>
                  Message{" "}
                  <span className="optional-label">
                    (optional)
                  </span>
                </label>

                <textarea
                  value={
                    followUpForm.message
                  }
                  onChange={(event) =>
                    setFollowUpForm({
                      ...followUpForm,
                      message:
                        event.target.value,
                    })
                  }
                  placeholder="Follow up regarding the customer's property requirement."
                  rows={4}
                  disabled={schedulingFollowUp}
                />

                <small>
                  If left blank, the AI can generate
                  a personalized message when the
                  follow-up becomes due.
                </small>

              </div>


              <div className="form-group">

                <label>
                  Notes{" "}
                  <span className="optional-label">
                    (optional)
                  </span>
                </label>

                <textarea
                  value={
                    followUpForm.notes
                  }
                  onChange={(event) =>
                    setFollowUpForm({
                      ...followUpForm,
                      notes:
                        event.target.value,
                    })
                  }
                  placeholder="Any internal notes for this follow-up..."
                  rows={3}
                  disabled={schedulingFollowUp}
                />

              </div>


              <div className="form-actions">

                <button
                  type="button"
                  className="cancel-button"
                  onClick={() =>
                    setShowFollowUp(false)
                  }
                  disabled={schedulingFollowUp}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="submit-lead-button"
                  disabled={schedulingFollowUp}
                >
                  {schedulingFollowUp
                    ? "Scheduling..."
                    : "Schedule Follow-up"}
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;
