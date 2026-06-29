import {
  buildForecastCellsFromSeries,
  type PredictionSeries,
} from "../prediction-series";
import {
  buildDampedLogTrendForecast,
  roundForecast,
  type DampedTrendForecast,
} from "../forecast-models";
import { requireLedgerTarget } from "../ledger-targets";
import type {
  ForecastCell,
  ForecastComparisonRun,
  PredictionPackSet,
} from "../forecast-cells";

const OCCUPATION_WAGE_NO_PACK_SET = {
  packSetId: "pack_set.occupation_wage_pressure_control.v1",
  label: "Occupation wage pressure control",
  mode: "none",
  packs: [],
  notes:
    "Control run using OEWS wage context and broad nominal wage-pressure signals without a BLS occupational wage projection pack.",
} satisfies PredictionPackSet;

const RECORDED_OCCUPATION_WAGE_RUN = {
  kind: "recorded-agent-run",
  runAt: "2026-06-21T13:35:00-04:00",
  agent: "brier-occupation-wage-pressure",
  model: "Codex recorded source-context synthesis",
  sourceContext: [
    "BLS OEWS May 2025 national annual wage tables",
    "BLS OEWS time-series API annual wage datatypes",
    "Employment Cost Index and average hourly earnings context",
    "SOC major occupational groups",
    "Task automation exposure literature",
  ],
  runLabel: "Occupation wage pressure - no projection pack",
  runDescription:
    "Control run over May 2026 OEWS annual wage statistics. BLS publishes current occupational wages but does not publish an official 2026 occupational wage projection.",
  packSet: OCCUPATION_WAGE_NO_PACK_SET,
} satisfies PredictionSeries["predictionRun"];

const BLS_CES_PRIVATE_AHE_MAY_2025 = 36.28;
const BLS_CES_PRIVATE_AHE_MAY_2026 = 37.53;
const BLS_CES_AHE_WAGE_GROWTH_LOG_PRIOR = Math.log(
  BLS_CES_PRIVATE_AHE_MAY_2026 / BLS_CES_PRIVATE_AHE_MAY_2025,
);
const BLS_CES_AHE_WAGE_GROWTH_PRIOR_LABEL =
  "BLS CES total private average hourly earnings, May 2025 to May 2026";

type OccupationWageStatistic =
  | "p10"
  | "p25"
  | "median"
  | "mean"
  | "p75"
  | "p90";

interface OccupationWageDefinition {
  socCode: string;
  slug: string;
  title: string;
  question: string;
  measure: string;
  statistic: OccupationWageStatistic;
  statisticLabel: string;
  statisticSlug: string;
  dataPointStatistic: string;
  blsField:
    | "A_PCT10"
    | "A_PCT25"
    | "A_MEDIAN"
    | "A_MEAN"
    | "A_PCT75"
    | "A_PCT90";
  datatypeCode: "11" | "12" | "13" | "04" | "14" | "15";
  whyItMatters: string;
  drivers: string[];
  latestAnnualWage: number;
  pointEstimate: number;
  ciLow: number;
  ciHigh: number;
  forecastModel: DampedTrendForecast;
  wageSignalResult: string;
  rationale: string;
}

interface OccupationWageGroupInput {
  socCode: string;
  slugBase: string;
  titleBase: string;
  label: string;
  measureLabel: string;
  whyItMatters: string;
  drivers: string[];
  latestMedianAnnualWage: number;
  signalTag: string;
  centralCase: string;
  downsideCase: string;
  latestMeanAnnualWage: number;
  latestP10AnnualWage: number;
  latestP25AnnualWage: number;
  latestP75AnnualWage: number;
  latestP90AnnualWage: number;
}

const OCCUPATION_WAGE_STATISTICS = {
  p10: {
    slug: "10th-percentile",
    label: "10th percentile",
    dataPointStatistic: "10th_percentile",
    blsField: "A_PCT10",
    datatypeCode: "11",
    valueKey: "latestP10AnnualWage",
  },
  p25: {
    slug: "25th-percentile",
    label: "25th percentile",
    dataPointStatistic: "25th_percentile",
    blsField: "A_PCT25",
    datatypeCode: "12",
    valueKey: "latestP25AnnualWage",
  },
  median: {
    slug: "median",
    label: "median",
    dataPointStatistic: "median",
    blsField: "A_MEDIAN",
    datatypeCode: "13",
    valueKey: "latestMedianAnnualWage",
  },
  mean: {
    slug: "mean",
    label: "mean",
    dataPointStatistic: "mean",
    blsField: "A_MEAN",
    datatypeCode: "04",
    valueKey: "latestMeanAnnualWage",
  },
  p75: {
    slug: "75th-percentile",
    label: "75th percentile",
    dataPointStatistic: "75th_percentile",
    blsField: "A_PCT75",
    datatypeCode: "14",
    valueKey: "latestP75AnnualWage",
  },
  p90: {
    slug: "90th-percentile",
    label: "90th percentile",
    dataPointStatistic: "90th_percentile",
    blsField: "A_PCT90",
    datatypeCode: "15",
    valueKey: "latestP90AnnualWage",
  },
} satisfies Record<
  OccupationWageStatistic,
  {
    slug: string;
    label: string;
    dataPointStatistic: string;
    blsField: OccupationWageDefinition["blsField"];
    datatypeCode: OccupationWageDefinition["datatypeCode"];
    valueKey: keyof Pick<
      OccupationWageGroupInput,
      | "latestP10AnnualWage"
      | "latestP25AnnualWage"
      | "latestMedianAnnualWage"
      | "latestMeanAnnualWage"
      | "latestP75AnnualWage"
      | "latestP90AnnualWage"
    >;
  }
>;

const OCCUPATION_WAGE_GROUPS = [
  {
    socCode: "11-0000",
    slugBase: "management",
    titleBase: "Management",
    label: "Management Occupations",
    measureLabel: "management occupations",
    whyItMatters:
      "Management wages help distinguish broad nominal wage pressure from composition effects in higher-paid supervisory and executive work.",
    drivers: [
      "Executive and managerial labor demand",
      "Professional-services margins",
      "AI-assisted management productivity",
      "Occupational composition",
    ],
    latestMedianAnnualWage: 126520,
    latestMeanAnnualWage: 145260,
    latestP10AnnualWage: 60130,
    latestP25AnnualWage: 82970,
    latestP75AnnualWage: 176280,
    latestP90AnnualWage: 257310,
    signalTag: "managerial_mix_and_professional_demand",
    centralCase:
      "steady managerial pay growth and a slightly higher-skill occupational mix",
    downsideCase:
      "The lower tail covers weaker white-collar hiring and margin pressure in professional services.",
  },
  {
    socCode: "13-0000",
    slugBase: "business-financial",
    titleBase: "Business and financial",
    label: "Business and Financial Operations Occupations",
    measureLabel: "business and financial operations occupations",
    whyItMatters:
      "This is a wage-side companion to the white-collar employment target: AI may compress routine analyst, compliance, bookkeeping, and claims work while leaving a higher-skill occupational mix.",
    drivers: [
      "Nominal wage growth",
      "Professional-services labor demand",
      "Finance and compliance skill mix",
      "AI-assisted back-office productivity",
    ],
    latestMedianAnnualWage: 82660,
    latestMeanAnnualWage: 95230,
    latestP10AnnualWage: 48820,
    latestP25AnnualWage: 62940,
    latestP75AnnualWage: 114820,
    latestP90AnnualWage: 153990,
    signalTag: "higher_skill_mix_supports_median",
    centralCase:
      "continued demand for analysts, compliance workers, and project management specialists",
    downsideCase:
      "The lower tail covers weaker professional hiring and lower bonus-sensitive finance demand.",
  },
  {
    socCode: "15-0000",
    slugBase: "computer-math",
    titleBase: "Computer and mathematical",
    label: "Computer and Mathematical Occupations",
    measureLabel: "computer and mathematical occupations",
    whyItMatters:
      "This is the cleanest wage target for whether AI tools are mainly labor-saving in software tasks or demand-expanding through AI infrastructure, security, data, and integration work.",
    drivers: [
      "Software labor demand",
      "AI infrastructure and security hiring",
      "Coding-assistant productivity",
      "Tech-sector pay normalization",
    ],
    latestMedianAnnualWage: 109280,
    latestMeanAnnualWage: 120080,
    latestP10AnnualWage: 58200,
    latestP25AnnualWage: 78820,
    latestP75AnnualWage: 155830,
    latestP90AnnualWage: 191450,
    signalTag: "ai_infrastructure_and_security_vs_coding_productivity",
    centralCase:
      "AI infrastructure, cloud integration, and cybersecurity support offset by normalized tech hiring",
    downsideCase:
      "The lower tail covers coding-assistant productivity and a softer software labor market holding down the central wage path.",
  },
  {
    socCode: "17-0000",
    slugBase: "architecture-engineering",
    titleBase: "Architecture and engineering",
    label: "Architecture and Engineering Occupations",
    measureLabel: "architecture and engineering occupations",
    whyItMatters:
      "Architecture and engineering wages connect AI-assisted technical design to infrastructure, energy, manufacturing, and construction demand.",
    drivers: [
      "Infrastructure and energy investment",
      "Engineering services demand",
      "Design automation",
      "Manufacturing and construction cycle",
    ],
    latestMedianAnnualWage: 99520,
    latestMeanAnnualWage: 106830,
    latestP10AnnualWage: 58670,
    latestP25AnnualWage: 76560,
    latestP75AnnualWage: 130240,
    latestP90AnnualWage: 166490,
    signalTag: "engineering_services_and_design_automation",
    centralCase:
      "solid infrastructure and engineering-services demand with moderate design-tool productivity gains",
    downsideCase:
      "The lower tail covers a softer construction/manufacturing cycle and fewer high-pay project starts.",
  },
  {
    socCode: "19-0000",
    slugBase: "life-physical-social-science",
    titleBase: "Life, physical, and social science",
    label: "Life, Physical, and Social Science Occupations",
    measureLabel: "life, physical, and social science occupations",
    whyItMatters:
      "Science wages are a useful white-collar benchmark where research funding, biotech, energy, and public-sector demand matter more than clerical automation.",
    drivers: [
      "Research funding",
      "Biotech and energy demand",
      "Public-sector hiring",
      "AI-assisted research productivity",
    ],
    latestMedianAnnualWage: 82530,
    latestMeanAnnualWage: 94600,
    latestP10AnnualWage: 48420,
    latestP25AnnualWage: 62380,
    latestP75AnnualWage: 114460,
    latestP90AnnualWage: 155830,
    signalTag: "research_funding_and_ai_assisted_science",
    centralCase:
      "stable research labor demand and a modest mix shift toward specialized technical roles",
    downsideCase:
      "The lower tail covers tighter grant budgets and slower public-sector hiring.",
  },
  {
    socCode: "21-0000",
    slugBase: "community-social-service",
    titleBase: "Community and social service",
    label: "Community and Social Service Occupations",
    measureLabel: "community and social service occupations",
    whyItMatters:
      "Community and social service wages expose the low- and mid-wage care workforce where public funding, staffing shortages, and demand for human contact dominate.",
    drivers: [
      "Public and nonprofit funding",
      "Care workforce shortages",
      "Behavioral health demand",
      "Low-wage service wage floor",
    ],
    latestMedianAnnualWage: 58300,
    latestMeanAnnualWage: 63410,
    latestP10AnnualWage: 37970,
    latestP25AnnualWage: 46370,
    latestP75AnnualWage: 75910,
    latestP90AnnualWage: 97630,
    signalTag: "care_services_shortage_pressure",
    centralCase:
      "continued staffing pressure in behavioral health, counseling, and community services",
    downsideCase:
      "The lower tail covers constrained public budgets and nonprofit funding limits.",
  },
  {
    socCode: "23-0000",
    slugBase: "legal",
    titleBase: "Legal",
    label: "Legal Occupations",
    measureLabel: "legal occupations",
    whyItMatters:
      "Legal wages test whether document automation and AI research tools compress support tasks while preserving or increasing demand for higher-skill legal work.",
    drivers: [
      "Law firm and corporate legal demand",
      "AI legal research tools",
      "Paralegal and support composition",
      "Professional-services pricing",
    ],
    latestMedianAnnualWage: 102500,
    latestMeanAnnualWage: 139510,
    latestP10AnnualWage: 49400,
    latestP25AnnualWage: 64800,
    latestP75AnnualWage: 174620,
    latestP90AnnualWage: 287070,
    signalTag: "legal_ai_composition_shift",
    centralCase:
      "moderate professional wage growth with a composition shift away from lower-paid routine document work",
    downsideCase:
      "The lower tail covers slower legal demand and stronger task substitution in research and drafting.",
  },
  {
    socCode: "25-0000",
    slugBase: "education-library",
    titleBase: "Educational instruction and library",
    label: "Educational Instruction and Library Occupations",
    measureLabel: "educational instruction and library occupations",
    whyItMatters:
      "Education and library wages give Thesis a public-sector-heavy wage target where budget cycles, staffing pressure, and AI tutoring tools interact.",
    drivers: [
      "State and local education budgets",
      "Teacher labor supply",
      "Higher education staffing",
      "AI tutoring and content tools",
    ],
    latestMedianAnnualWage: 60570,
    latestMeanAnnualWage: 67540,
    latestP10AnnualWage: 32990,
    latestP25AnnualWage: 43900,
    latestP75AnnualWage: 79470,
    latestP90AnnualWage: 105240,
    signalTag: "education_budget_and_staffing_pressure",
    centralCase:
      "continued teacher and instructor wage pressure within state and local budget constraints",
    downsideCase:
      "The lower tail covers weak education budgets and limited salary schedule increases.",
  },
  {
    socCode: "27-0000",
    slugBase: "arts-media",
    titleBase: "Arts, design, entertainment, sports, and media",
    label: "Arts, Design, Entertainment, Sports, and Media Occupations",
    measureLabel: "arts, design, entertainment, sports, and media occupations",
    whyItMatters:
      "Arts and media wages are a direct creative-work target for generative AI exposure, advertising demand, and platform-driven composition changes.",
    drivers: [
      "Advertising and media demand",
      "Generative AI creative tools",
      "Entertainment production cycle",
      "Freelance and platform composition",
    ],
    latestMedianAnnualWage: 62750,
    latestMeanAnnualWage: 79790,
    latestP10AnnualWage: 34700,
    latestP25AnnualWage: 44720,
    latestP75AnnualWage: 94530,
    latestP90AnnualWage: 134900,
    signalTag: "creative_ai_and_media_demand",
    centralCase:
      "positive nominal wage growth partly offset by weak media hiring and creative-task automation",
    downsideCase:
      "The lower tail covers continued advertising softness and substitution in routine design and content tasks.",
  },
  {
    socCode: "29-0000",
    slugBase: "healthcare-practitioners-technical",
    titleBase: "Healthcare practitioners and technical",
    label: "Healthcare Practitioners and Technical Occupations",
    measureLabel: "healthcare practitioners and technical occupations",
    whyItMatters:
      "Healthcare practitioner wages are a high-demand, licensure-heavy comparator where demographics and care utilization should dominate near-term AI substitution.",
    drivers: [
      "Care utilization",
      "Licensed clinician shortages",
      "Hospital and clinic margins",
      "AI clinical workflow tools",
    ],
    latestMedianAnnualWage: 86530,
    latestMeanAnnualWage: 108700,
    latestP10AnnualWage: 46270,
    latestP25AnnualWage: 63860,
    latestP75AnnualWage: 123540,
    latestP90AnnualWage: 171790,
    signalTag: "licensed_healthcare_shortage_pressure",
    centralCase:
      "strong care demand and licensure constraints supporting above-average wage growth",
    downsideCase:
      "The lower tail covers provider margin pressure and slower hiring in lower-margin settings.",
  },
  {
    socCode: "31-0000",
    slugBase: "healthcare-support",
    titleBase: "Healthcare support",
    label: "Healthcare Support Occupations",
    measureLabel: "healthcare support occupations",
    whyItMatters:
      "Healthcare support gives Thesis a low-wage, low-substitution wage target where staffing scarcity and minimum-wage pressure can matter more than software substitution.",
    drivers: [
      "Care staffing shortages",
      "Medicaid and Medicare utilization",
      "Low-wage service wage floor",
      "Limited physical-task automation",
    ],
    latestMedianAnnualWage: 38340,
    latestMeanAnnualWage: 40800,
    latestP10AnnualWage: 28980,
    latestP25AnnualWage: 34320,
    latestP75AnnualWage: 45930,
    latestP90AnnualWage: 54230,
    signalTag: "high_staffing_pressure_low_automation_substitution",
    centralCase: "strong care demand and low-wage service recruitment pressure",
    downsideCase:
      "The lower tail reflects provider margin constraints and state-level Medicaid funding pressure.",
  },
  {
    socCode: "33-0000",
    slugBase: "protective-service",
    titleBase: "Protective service",
    label: "Protective Service Occupations",
    measureLabel: "protective service occupations",
    whyItMatters:
      "Protective service wages add a public-safety and security benchmark where staffing, public budgets, and physical presence requirements matter.",
    drivers: [
      "Public safety staffing",
      "State and local budgets",
      "Private security demand",
      "Overtime and shift premiums",
    ],
    latestMedianAnnualWage: 50080,
    latestMeanAnnualWage: 60720,
    latestP10AnnualWage: 32850,
    latestP25AnnualWage: 37350,
    latestP75AnnualWage: 75990,
    latestP90AnnualWage: 102470,
    signalTag: "public_safety_staffing_pressure",
    centralCase:
      "continued staffing pressure in public safety and private security roles",
    downsideCase:
      "The lower tail covers tight state and local budgets and weaker private security demand.",
  },
  {
    socCode: "35-0000",
    slugBase: "food-prep-serving",
    titleBase: "Food preparation and serving",
    label: "Food Preparation and Serving Related Occupations",
    measureLabel: "food preparation and serving related occupations",
    whyItMatters:
      "Food-service wages are a low-wage service benchmark for wage-floor pressure, consumer demand, and partial automation in ordering and kitchen workflows.",
    drivers: [
      "Restaurant labor demand",
      "Minimum-wage and wage-floor pressure",
      "Food-service automation",
      "Consumer spending on services",
    ],
    latestMedianAnnualWage: 35050,
    latestMeanAnnualWage: 37150,
    latestP10AnnualWage: 23120,
    latestP25AnnualWage: 28760,
    latestP75AnnualWage: 41860,
    latestP90AnnualWage: 51340,
    signalTag: "low_wage_service_wage_floor",
    centralCase:
      "continued wage-floor pressure in restaurants and other consumer services",
    downsideCase:
      "The lower tail covers weaker restaurant traffic and more aggressive labor-saving service technology.",
  },
  {
    socCode: "37-0000",
    slugBase: "building-grounds",
    titleBase: "Building and grounds cleaning and maintenance",
    label: "Building and Grounds Cleaning and Maintenance Occupations",
    measureLabel: "building and grounds cleaning and maintenance occupations",
    whyItMatters:
      "Building and grounds wages track local service labor pressure in cleaning, maintenance, and grounds work where tasks remain largely physical.",
    drivers: [
      "Facilities service demand",
      "Low-wage labor supply",
      "Real estate occupancy",
      "Limited physical-task automation",
    ],
    latestMedianAnnualWage: 37680,
    latestMeanAnnualWage: 40880,
    latestP10AnnualWage: 29010,
    latestP25AnnualWage: 33930,
    latestP75AnnualWage: 46170,
    latestP90AnnualWage: 57420,
    signalTag: "physical_service_labor_pressure",
    centralCase:
      "low-wage service labor pressure with limited near-term automation substitution",
    downsideCase:
      "The lower tail covers weaker commercial real estate occupancy and facilities demand.",
  },
  {
    socCode: "39-0000",
    slugBase: "personal-care-service",
    titleBase: "Personal care and service",
    label: "Personal Care and Service Occupations",
    measureLabel: "personal care and service occupations",
    whyItMatters:
      "Personal care wages are a human-service benchmark where in-person work, demographics, and low-wage labor supply are central.",
    drivers: [
      "Personal services demand",
      "Low-wage labor supply",
      "Demographic care demand",
      "Limited in-person task automation",
    ],
    latestMedianAnnualWage: 36410,
    latestMeanAnnualWage: 41070,
    latestP10AnnualWage: 26430,
    latestP25AnnualWage: 30820,
    latestP75AnnualWage: 46060,
    latestP90AnnualWage: 61020,
    signalTag: "in_person_service_wage_pressure",
    centralCase:
      "continued wage-floor pressure in in-person personal and care services",
    downsideCase:
      "The lower tail covers weaker discretionary personal-service spending.",
  },
  {
    socCode: "41-0000",
    slugBase: "sales",
    titleBase: "Sales and related",
    label: "Sales and Related Occupations",
    measureLabel: "sales and related occupations",
    whyItMatters:
      "Sales wages connect retail, call-center, and business-development task exposure to consumer demand and online substitution.",
    drivers: [
      "Retail and consumer demand",
      "E-commerce substitution",
      "AI sales-support tools",
      "Commission-heavy composition",
    ],
    latestMedianAnnualWage: 38530,
    latestMeanAnnualWage: 54960,
    latestP10AnnualWage: 28080,
    latestP25AnnualWage: 32440,
    latestP75AnnualWage: 61100,
    latestP90AnnualWage: 99850,
    signalTag: "sales_tools_and_retail_mix",
    centralCase:
      "moderate nominal wage growth offset by retail automation and e-commerce pressure",
    downsideCase:
      "The lower tail covers weaker retail demand and a lower-commission occupational mix.",
  },
  {
    socCode: "43-0000",
    slugBase: "office-admin",
    titleBase: "Office and administrative support",
    label: "Office and Administrative Support Occupations",
    measureLabel: "office and administrative support occupations",
    whyItMatters:
      "Office and administrative support is the wage counterpart to the clearest clerical automation employment target, so it helps separate headcount decline from composition and wage-pressure effects.",
    drivers: [
      "Clerical automation",
      "Service-sector administrative demand",
      "Occupational composition",
      "Nominal wage growth",
    ],
    latestMedianAnnualWage: 47450,
    latestMeanAnnualWage: 51560,
    latestP10AnnualWage: 33530,
    latestP25AnnualWage: 38540,
    latestP75AnnualWage: 60060,
    latestP90AnnualWage: 76170,
    signalTag: "routine_low_wage_roles_shrink_first",
    centralCase:
      "nominal wage growth and composition effects from routine lower-wage roles shrinking first",
    downsideCase:
      "The lower tail covers weaker service-sector administrative demand and broad clerical substitution.",
  },
  {
    socCode: "45-0000",
    slugBase: "farming-fishing-forestry",
    titleBase: "Farming, fishing, and forestry",
    label: "Farming, Fishing, and Forestry Occupations",
    measureLabel: "farming, fishing, and forestry occupations",
    whyItMatters:
      "Farming, fishing, and forestry wages add a goods-producing, outdoor-work benchmark exposed to seasonal labor supply and mechanization.",
    drivers: [
      "Agricultural labor supply",
      "Seasonal and migrant labor conditions",
      "Commodity and food demand",
      "Mechanization",
    ],
    latestMedianAnnualWage: 36630,
    latestMeanAnnualWage: 41510,
    latestP10AnnualWage: 31760,
    latestP25AnnualWage: 34540,
    latestP75AnnualWage: 44990,
    latestP90AnnualWage: 58220,
    signalTag: "agricultural_labor_supply_pressure",
    centralCase:
      "continued low-wage labor pressure in seasonal and outdoor work",
    downsideCase:
      "The lower tail covers weaker commodity demand and more labor-saving mechanization.",
  },
  {
    socCode: "47-0000",
    slugBase: "construction-extraction",
    titleBase: "Construction and extraction",
    label: "Construction and Extraction Occupations",
    measureLabel: "construction and extraction occupations",
    whyItMatters:
      "Construction and extraction wages measure skilled-trades pressure tied to infrastructure, housing, energy, and limited short-run task automation.",
    drivers: [
      "Infrastructure and construction demand",
      "Skilled-trades labor supply",
      "Housing cycle",
      "Energy and extraction activity",
    ],
    latestMedianAnnualWage: 59540,
    latestMeanAnnualWage: 65360,
    latestP10AnnualWage: 38100,
    latestP25AnnualWage: 46880,
    latestP75AnnualWage: 77970,
    latestP90AnnualWage: 101650,
    signalTag: "skilled_trades_shortage_pressure",
    centralCase:
      "skilled-trades shortages and infrastructure demand supporting wage growth",
    downsideCase:
      "The lower tail covers a weaker housing cycle and slower project starts.",
  },
  {
    socCode: "49-0000",
    slugBase: "installation-maintenance-repair",
    titleBase: "Installation, maintenance, and repair",
    label: "Installation, Maintenance, and Repair Occupations",
    measureLabel: "installation, maintenance, and repair occupations",
    whyItMatters:
      "Installation and repair wages track hands-on technical work that may benefit from AI diagnostics while remaining hard to automate physically.",
    drivers: [
      "Skilled technical labor supply",
      "Equipment and vehicle repair demand",
      "AI diagnostic tools",
      "Goods and infrastructure cycle",
    ],
    latestMedianAnnualWage: 59620,
    latestMeanAnnualWage: 63320,
    latestP10AnnualWage: 37000,
    latestP25AnnualWage: 46110,
    latestP75AnnualWage: 76670,
    latestP90AnnualWage: 96540,
    signalTag: "hands_on_technical_shortage_pressure",
    centralCase:
      "shortages in hands-on technical roles and steady repair demand",
    downsideCase:
      "The lower tail covers weaker goods activity and productivity gains from diagnostic tools.",
  },
  {
    socCode: "51-0000",
    slugBase: "production",
    titleBase: "Production",
    label: "Production Occupations",
    measureLabel: "production occupations",
    whyItMatters:
      "Production wages connect automation to manufacturing labor demand, robotics, reshoring, union contracts, and goods-sector cyclicality rather than only information-work substitution.",
    drivers: [
      "Manufacturing labor demand",
      "Union and shortage wage pressure",
      "Factory automation",
      "Goods-sector cycle",
    ],
    latestMedianAnnualWage: 46990,
    latestMeanAnnualWage: 51600,
    latestP10AnnualWage: 34240,
    latestP25AnnualWage: 38130,
    latestP75AnnualWage: 59920,
    latestP90AnnualWage: 76990,
    signalTag: "process_control_robotics_and_skilled_production_shortages",
    centralCase:
      "shortages in skilled production roles and existing wage contracts offsetting automation pressure",
    downsideCase:
      "The lower tail covers mixed manufacturing demand and faster process-control or robotics productivity gains.",
  },
  {
    socCode: "53-0000",
    slugBase: "transport-material-moving",
    titleBase: "Transportation and material moving",
    label: "Transportation and Material Moving Occupations",
    measureLabel: "transportation and material moving occupations",
    whyItMatters:
      "This wage target tracks logistics, warehousing, driving, routing, and material movement where automation can change task mix before full autonomy changes employment.",
    drivers: [
      "Warehouse and logistics demand",
      "Routing and warehouse automation",
      "Driver wage pressure",
      "Goods movement volume",
    ],
    latestMedianAnnualWage: 44350,
    latestMeanAnnualWage: 49850,
    latestP10AnnualWage: 31060,
    latestP25AnnualWage: 36290,
    latestP75AnnualWage: 55990,
    latestP90AnnualWage: 72440,
    signalTag: "warehouse_routing_and_driver_wage_pressure",
    centralCase:
      "driver and material-moving demand offset by warehouse automation and routing tools",
    downsideCase:
      "The lower tail covers weaker goods movement volume and faster logistics automation.",
  },
] satisfies OccupationWageGroupInput[];

function occupationWageDefinitionFor(
  group: OccupationWageGroupInput,
  statistic: OccupationWageStatistic,
): OccupationWageDefinition {
  const statisticConfig = OCCUPATION_WAGE_STATISTICS[statistic];
  const latestAnnualWage = group[statisticConfig.valueKey];
  const forecastModel = roundForecast(
    buildDampedLogTrendForecast([{ period: 2025, value: latestAnnualWage }], {
      fallbackGrowth: BLS_CES_AHE_WAGE_GROWTH_LOG_PRIOR,
      fallbackLabel: BLS_CES_AHE_WAGE_GROWTH_PRIOR_LABEL,
      residualStdDevFloor: 0.04,
    }),
    100,
  );

  return {
    socCode: group.socCode,
    slug: `oews-${group.slugBase}-${statisticConfig.slug}-wage-may-2026`,
    title: `${group.titleBase} ${statisticConfig.label} wage, May 2026`,
    question:
      `What annual ${statisticConfig.label} wage will BLS first publish for ` +
      `SOC ${group.socCode} ${group.label} in the May 2026 national OEWS release?`,
    measure: `National annual ${statisticConfig.label} wage for ${group.measureLabel}`,
    statistic,
    statisticLabel: statisticConfig.label,
    statisticSlug: statisticConfig.slug,
    dataPointStatistic: statisticConfig.dataPointStatistic,
    blsField: statisticConfig.blsField,
    datatypeCode: statisticConfig.datatypeCode,
    whyItMatters: group.whyItMatters,
    drivers: group.drivers,
    latestAnnualWage,
    pointEstimate: forecastModel.pointEstimate,
    ciLow: forecastModel.ciLow,
    ciHigh: forecastModel.ciHigh,
    forecastModel,
    wageSignalResult:
      `{ base_${statistic}_wage_2025_usd: ${latestAnnualWage}, ` +
      `model: '${forecastModel.modelId}', status: '${forecastModel.status}', ` +
      `growth_prior: '${BLS_CES_AHE_WAGE_GROWTH_PRIOR_LABEL}', ` +
      `annualized_log_growth: '${formatPercent(forecastModel.annualizedGrowth)}', ` +
      `occupation_signal: '${group.signalTag}' }`,
    rationale:
      `The forecast is produced by ${forecastModel.modelId}. The OEWS API ` +
      `returns one target-specific ${statisticConfig.label} observation for ` +
      `this current SOC/statistic series, so the model records fallback status ` +
      `instead of fitting a false trend. It applies the broad wage-growth prior ` +
      `from ${BLS_CES_AHE_WAGE_GROWTH_PRIOR_LABEL} and keeps a volatility-floor ` +
      `interval. The occupation-specific qualitative overlay is ${group.centralCase}. ${group.downsideCase}`,
  };
}

const OCCUPATION_WAGE_DEFINITIONS: OccupationWageDefinition[] =
  OCCUPATION_WAGE_GROUPS.flatMap((group) =>
    (
      [
        "p10",
        "p25",
        "median",
        "mean",
        "p75",
        "p90",
      ] satisfies OccupationWageStatistic[]
    ).map((statistic) => occupationWageDefinitionFor(group, statistic)),
  );

function oewsWageDataPointId(
  socCode: string,
  statistic: OccupationWageStatistic,
): string {
  const statisticConfig = OCCUPATION_WAGE_STATISTICS[statistic];
  return `bls.oews.national_occupation_${statisticConfig.dataPointStatistic}_annual_wage.soc_${socCode.replace("-", "_")}.may_2026.first_print`;
}

function oewsAnnualWageSeriesId(
  socCode: string,
  datatypeCode: OccupationWageDefinition["datatypeCode"],
): string {
  return `OEUN0000000000000${socCode.replace("-", "")}${datatypeCode}`;
}

function occupationWageSeriesFor(
  definition: OccupationWageDefinition,
): PredictionSeries {
  const target = requireLedgerTarget(
    oewsWageDataPointId(definition.socCode, definition.statistic),
  );
  const seriesId = oewsAnnualWageSeriesId(
    definition.socCode,
    definition.datatypeCode,
  );

  return {
    seriesId: target.dataPointId.replace(".may_2026.first_print", ""),
    title: definition.title,
    measure: definition.measure,
    unit: target.unit,
    source: target.source,
    sourceUrl: target.sourceUrl,
    cadence: "annual",
    priority: "P1",
    resolutionLatency: "~12 months",
    resolutionPolicy: target.resolutionPolicy,
    benchmark: `May 2025 OEWS national annual ${definition.statisticLabel} wage plus nominal wage-growth and composition priors`,
    chainableQuestions: [
      "next annual release",
      "mean wage",
      "median wage",
      "percentile wages",
      "detailed SOC rows",
    ],
    whyItMatters: definition.whyItMatters,
    drivers: definition.drivers,
    history: [
      {
        label: `May 2025 OEWS ${definition.statisticLabel}`,
        value: definition.latestAnnualWage,
      },
    ],
    historyTool: {
      tool: "bls.oews.api",
      call: `bls.oews.api({ seriesId: "${seriesId}", release: "May 2025", datatype: "Annual ${definition.statisticLabel} wage" })`,
      result: `{ series_id: '${seriesId}', year: 2025, period: 'A01', annual_${definition.statistic}_wage_usd: ${definition.latestAnnualWage} }`,
    },
    predictionRun: RECORDED_OCCUPATION_WAGE_RUN,
    targets: [
      {
        slug: definition.slug,
        title: definition.title,
        question: definition.question,
        dataPointId: target.dataPointId,
        horizon: "next_release",
        horizonLabel: "May 2026 OEWS first print",
        periodLabel: target.periodLabel,
        resolutionDate: target.resolutionDate,
        resolutionRule: target.resolutionRule,
        resolutionSourceUrl: target.resolutionSourceUrl,
        pointEstimate: definition.pointEstimate,
        ciLow: definition.ciLow,
        ciHigh: definition.ciHigh,
        tools: [
          {
            tool: "bls.oews.source",
            call: `bls.oews.source({ release: "May 2026", geography: "national", occupation: "${definition.socCode}", field: "${definition.blsField}" })`,
            result: `Target registered in the Thesis ledger before forecasting; resolution uses the first-published BLS national OEWS annual ${definition.statisticLabel} wage field.`,
          },
          {
            tool: "forecast_model.damped_log_trend",
            call: `damped_log_trend_v1({ soc_major_group: "${definition.socCode}", statistic: "${definition.statistic}", base_year: 2025, target_year: 2026 })`,
            result: definition.wageSignalResult,
          },
        ],
        rationale: definition.rationale,
      },
    ],
  };
}

export const OEWS_OCCUPATION_WAGE_PREDICTION_SERIES =
  OCCUPATION_WAGE_DEFINITIONS.map(occupationWageSeriesFor);

export const OCCUPATION_WAGE_EXAMPLES = buildForecastCellsFromSeries(
  OEWS_OCCUPATION_WAGE_PREDICTION_SERIES,
).map(withCurrentOewsWageBaselineRun);

function withCurrentOewsWageBaselineRun(forecast: ForecastCell): ForecastCell {
  const definition = OCCUPATION_WAGE_DEFINITIONS.find(
    (candidate) => candidate.slug === forecast.slug,
  );
  if (!definition) return forecast;

  return {
    ...forecast,
    comparisonRuns: [
      ...(forecast.comparisonRuns ?? []),
      buildCurrentOewsWageBaselineRun(forecast, definition),
    ],
  };
}

function buildCurrentOewsWageBaselineRun(
  forecast: ForecastCell,
  definition: OccupationWageDefinition,
): ForecastComparisonRun {
  const point = definition.latestAnnualWage;
  const epsilon = 500;

  return {
    variantId: "may-2025-oews-carry-forward",
    label: "May 2025 OEWS carry-forward",
    description: `Baseline comparator: carry the latest published OEWS annual ${definition.statisticLabel} wage forward unchanged.`,
    pointEstimate: point,
    ciLow: point - epsilon,
    ciHigh: point + epsilon,
    drivers: [
      `Latest published OEWS annual ${definition.statisticLabel} wage`,
      "No explicit occupational wage projection",
      "Flat nominal carry-forward comparator",
    ],
    predictionRun: {
      kind: "recorded-agent-run",
      runAt: "2026-05-15T10:00:00-04:00",
      agent: "BLS OEWS current table",
      model: `May 2025 annual ${definition.statisticLabel} wage carry-forward baseline`,
      sourceContext: [
        `BLS OEWS May 2025 national annual ${definition.statisticLabel} wage table`,
        `BLS OEWS time-series API datatype ${definition.datatypeCode} annual ${definition.statisticLabel} wage`,
      ],
      runLabel: "Current OEWS carry-forward",
      runDescription:
        "Not an official BLS forecast; a flat comparator because BLS does not publish projected occupational wage levels.",
    },
    reasoning: [
      {
        kind: "heading",
        text: "Current-wage comparator",
      },
      {
        kind: "text",
        text: `BLS publishes current OEWS occupational wages but not an official May 2026 occupational wage projection. This comparator carries the May 2025 ${definition.statisticLabel} annual wage forward unchanged.`,
      },
      {
        kind: "tool",
        tool: "bls.oews.api",
        call: `bls.oews.api({ target: "${forecast.dataPointId}", comparator: "latest_observed_${definition.blsField.toLowerCase()}" })`,
        result: `{ latest_observed_year: 2025, annual_${definition.statistic}_wage_usd: ${point}, source: 'BLS OEWS May 2025' }`,
      },
      {
        kind: "math",
        text: `Flat carry-forward baseline = ${formatUsd(point)}.`,
      },
      {
        kind: "forecast",
        point,
        ciLow: point - epsilon,
        ciHigh: point + epsilon,
      },
    ],
  };
}

function formatUsd(value: number): string {
  return `$${Math.round(value).toLocaleString("en-US")}`;
}

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}
