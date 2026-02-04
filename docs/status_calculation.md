# Status and Discount Calculation Logic

## Status Calculation Logic

The application status is determined using the following logic:

### Input Factors
* **Application Data**: Information from the application record
* **Requires Approval Flag**: Configuration from the popup city settings
* **Reviews Status**: The calculated status from reviews (if applicable)

### Status Determination Rules

1. **Withdrawn or Rejected**
   * If reviews status is `WITHDRAWN` or `REJECTED`, this status is used regardless of other factors.

2. **Non-Approval Applications**
   * If the popup city does not require approval AND the applicant did not request a discount, the status is set to `ACCEPTED`.

3. **Draft or In-Review Applications**
   * If no reviews status exists OR a discount was requested but not assigned yet, the status will be:
     * `IN_REVIEW` if the application has been submitted
     * `DRAFT` if the application has not been submitted

4. **Other Cases**
   * In all other cases, the reviews status is used.

## Discount Request Determination
A discount is considered requested when:
* For popup cities that require approval: If the scholarship request field is set
* For popup cities that don't require approval: If the applicant is a renter OR has a scholarship request

## Implementation Details

The status calculation is implemented in the `calculate_status` function in `app/api/applications/crud.py`. This function:

1. Takes the application object, requires_approval flag, and optional reviews_status as inputs
2. Determines if a discount was requested using the `_requested_a_discount` function
3. Applies the rules above to calculate the appropriate status
4. Returns both the calculated status and a boolean indicating if a discount was requested

The discount request determination is implemented in the `_requested_a_discount` function, which checks:
* If the popup city requires approval: Returns application.scholarship_request
* If the popup city doesn't require approval: Returns application.is_renter OR application.scholarship_request

This logic ensures applications flow through the correct statuses based on their requirements and submission state.

## NocoDB Calculated Status

The reviews status referenced above is a calculated column (`calculated_status`) in NocoDB. This status is determined by a formula that evaluates reviewer inputs and application state:

1. If the applicant is not attending (`not_attending == 1`), status is `WITHDRAWN`
2. If the application is auto-approved (`auto_approved == 1`), status is `ACCEPTED`
3. For applications requiring review:
   - Status is `ACCEPTED` if:
     - At least one reviewer gave a "strong yes", OR
     - At least two reviewers gave a "yes"
   - Status is `REJECTED` if:
     - At least one reviewer gave a "strong no", OR
     - At least two reviewers gave a "no"
   - Otherwise, no status is assigned (empty string)

The actual formula used in NocoDB is (reviewer fields: `sun_review`, `xiaoyu_review`, `frank_review`):
```
IF(({not_attending} == 1), "withdrawn",
  IF(({auto_approved} == 1), "accepted",
    IF(OR(
        OR(
          AND(({sun_review} == "yes"),
              OR(({xiaoyu_review} == "yes"), ({frank_review} == "yes"))),
          AND(({xiaoyu_review} == "yes"),
              OR(({sun_review} == "yes"), ({frank_review} == "yes"))),
          AND(({frank_review} == "yes"),
              OR(({sun_review} == "yes"), ({xiaoyu_review} == "yes")))
        ),
        OR(({sun_review} == "strong yes"), ({xiaoyu_review} == "strong yes"), ({frank_review} == "strong yes"))
      ), "accepted",
      IF(OR(
          OR(
            AND(({sun_review} == "no"),
                OR(({xiaoyu_review} == "no"), ({frank_review} == "no"))),
            AND(({xiaoyu_review} == "no"),
                OR(({sun_review} == "no"), ({frank_review} == "no"))),
            AND(({frank_review} == "no"),
                OR(({sun_review} == "no"), ({xiaoyu_review} == "no")))
          ),
          OR(({sun_review} == "strong no"), ({xiaoyu_review} == "strong no"), ({frank_review} == "strong no"))
        ), "rejected", "")
    )
  )
)
```

The formula above can be modified as needed to adjust the review logic or accommodate changes in the review process.

---

**← [Back to Documentation Index](./index.md)**