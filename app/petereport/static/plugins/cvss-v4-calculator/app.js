// Copyright FIRST, Red Hat, and contributors
// SPDX-License-Identifier: BSD-2-Clause

const app = Vue.createApp({
    data() {
        return {
            cvssConfigData: cvssConfig,
            maxComposedData: maxComposed,
            maxSeverityData: maxSeverity,
            expectedMetricOrder: expectedMetricOrder,
            cvssMacroVectorDetailsData: cvssMacroVectorDetails,
            cvssMacroVectorValuesData: cvssMacroVectorValues,
            showDetails: false,
            cvssSelected: null,
            header_height: 0,
            lookup: cvssLookup_global,
        }
    },
    methods: {
        buttonClass(isPrimary, big = false) {
            result = "btn btn-m"
            if (isPrimary) {
                result += " btn-primary"
            }
            if (!big) {
                result += " btn-sm"
            }

            return result
        },
        scoreClass(qualScore) {
            if (qualScore == "Low") {
                return "c-hand text-success"
            }
            else if (qualScore == "Medium") {
                return "c-hand text-warning"
            }
            else if (qualScore == "High") {
                return "c-hand text-error"
            }
            else if (qualScore == "Critical") {
                return "c-hand text-error text-bold"
            }
            else {
                return "c-hand text-gray"
            }
        },
        copyVector() {
            navigator.clipboard.writeText(this.vector)
            window.location.hash = this.vector
        },
        onButton(metric, value) {
            this.cvssSelected[metric] = value
            window.location.hash = this.vector
        },
        setButtonsToVector(vector) {
            this.resetSelected()
            metrics = vector.split("/")
            // Remove hash + CVSS v4.0 prefix
            prefix = metrics[0].slice(1);
            if (prefix != "CVSS:4.0") {
                console.log("Error invalid vector, missing CVSS v4.0 prefix")
                return
            }
            metrics.shift()

            // Ensure compliance first
            toSelect = {}
            oi = 0
            for (index in metrics) {
                [key, value] = metrics[index].split(":")

                expected = Object.entries(this.expectedMetricOrder)[oi++]
                while (true) {
                    // If out of possible metrics ordering, it not a valid value thus
                    // the vector is invalid
                    if (expected == undefined) {
                        console.log("Error invalid vector, too many metric values")
                        return
                    }
                    if (key != expected[0]) {
                        // If not this metric but is mandatory, the vector is invalid
                        // As the only mandatory ones are from the Base group, 11 is the
                        // number of metrics part of it.
                        if (oi <= 11) {
                            console.log("Error invalid vector, missing mandatory metrics")
                            return
                        }
                        // If a non-mandatory, retry
                        expected = Object.entries(this.expectedMetricOrder)[oi++]
                        continue
                    }
                    break
                }
                // The value MUST be part of the metric's values, case insensitive
                if (!expected[1].includes(value)) {
                    console.log("Error invalid vector, for key " + key + ", value " + value + " is not in " + expected[1])
                    return
                }
                if (key in this.cvssSelected) {
                    toSelect[key] = value
                }
            }

            // Apply iff is compliant
            for (key in toSelect) {
                this.cvssSelected[key] = toSelect[key]
            }
        },
        onReset() {
            window.location.hash = ""
        },
        resetSelected() {
            this.cvssSelected = {}
            for ([metricType, metricTypeData] of Object.entries(this.cvssConfigData)) {
                for ([metricGroup, metricGroupData] of Object.entries(metricTypeData.metric_groups)) {
                    for ([metric, metricData] of Object.entries(metricGroupData)) {
                        this.cvssSelected[metricData.short] = metricData.selected
                    }
                }
            }
        },
        splitObjectEntries(object, chunkSize) {
            arr = Object.entries(object)
            res = [];
            for (let i = 0; i < arr.length; i += chunkSize) {
                chunk = arr.slice(i, i + chunkSize)
                res.push(chunk)
            }
            return res
        }
    },
    computed: {
        vector() {
            value = "CVSS:4.0"
            for (metric in this.expectedMetricOrder) {
                selected = this.cvssSelected[metric]
                if (selected != "X") {
                    value = value.concat("/" + metric + ":" + selected)
                }
            }
            return value
        },
        score() {
            return cvss_score(
                this.cvssSelected,
                this.lookup,
                this.maxSeverityData)
        },
        qualScore() {
            if (this.score == 0) {
                return "None"
            }
            else if (this.score < 4.0) {
                return "Low"
            }
            else if (this.score < 7.0) {
                return "Medium"
            }
            else if (this.score < 9.0) {
                return "High"
            }
            else {
                return "Critical"
            }
        },
        console: () => console,
        window: () => window,
    },
    beforeMount() {
        this.resetSelected()
    },
    mounted() {
        this.setButtonsToVector(window.location.hash)
        window.addEventListener("hashchange", () => {
            this.setButtonsToVector(window.location.hash)
        })

        const resizeObserver = new ResizeObserver(() => {
            this.header_height = document.getElementById('header').clientHeight
        })

        resizeObserver.observe(document.getElementById('header'))
    },
    watch: {
        'vector': function() {
            var message = [this.score, this.qualScore, this.vector];
            window.top.postMessage(message, '*')
        }
    },
})

app.mount("#app")
